
import logging
import random
import time
import threading
import os
import binascii
import re
import types
import sys
from socket import gethostname

tracking_regex = re.compile("^[a-f0-9]{32}$")
logger = logging.getLogger(__name__)


def tracking_id_not_valid(track_id):
    try: return re.match(tracking_regex, track_id) is None
    except: return True


def _span_id_not_valid(span_id):
    try:
        num_list = str(span_id).split(".")
        for num in num_list:
            if not num.isdigit():
                return True

        return False
    except:
        return True

class Tracer(object):
    def __init__(self, **kwargs):
        sampling = kwargs.get('sampling', 1)
        assert 0 <= sampling and sampling <= 1, "Sampling must be between 0 and 1"

        self.aggregate_traces = kwargs.get('aggregate_traces', False),
        self.thread_local = threading.local()
        self.thread_local.initialized = False

        self.tracking_id_header = "X-Hulu-Request-Id"
        self.span_id_header = "Span-Id"
        self.enable_tracing = kwargs.get('aggregate_traces', True),
        self.sampling = sampling


    def initialize_request(self, request, url_args=False):
        try:
            headers = getattr(request, "headers", {})
            tracking_id = headers.get(self.tracking_id_header, binascii.b2a_hex(os.urandom(16)))
            if tracking_id_not_valid(tracking_id):
                tracking_id = binascii.b2a_hex(os.urandom(16))

            span_id = headers.get(self.span_id_header, "1")
            if _span_id_not_valid(span_id):
                span_id = "1"

            self.thread_local.monitor_request = random.random() < self.sampling
            self.thread_local.dependency_num = 1
            self.thread_local.tracking_id = tracking_id
            self.thread_local.span_id = span_id
            self.thread_local.events = []
            self.thread_local.initialized = True

            request_context = {
                "url_full" : request.url,
                "url_host" : request.host,

                "url_path" : request.path,
                "url_args" : request.args if url_args else {},

                "http_method" : request.method,
                "body" : request.form,
                "headers": {},
            }

            if self.track_request():
                event = {"category": "request_start", "context": request_context, "timestamp": time.time()}
                if self.aggregate_traces:
                    self.thread_local.events.append(event)
                else:
                    logger.info("starting request", extra=event)
        except Exception as ex:
            logger.exception("Failed to Initialize Request: %s" % ex)

    def trace(self, dependency_name, log_args=True, log_return=False):
        def outer(func):
            def inner(*args, **kwargs):
                if not getattr(self.thread_local, "initialized", False):
                    return func(*args, **kwargs)

                remote_span_id = "{0}.{1}".format(self.thread_local.span_id, self.thread_local.dependency_num)
                self.thread_local.remote_span_id = remote_span_id
                self.thread_local.dependency_num += 1

                start_event = {
                    "dependency_name" : dependency_name,
                    "function_name": func.__name__,
                    "dependency_span_id": remote_span_id,
                }

                if log_args:
                    start_event["args"] = [a for a in args if self.is_valid_json_type(a)]
                    start_event["kwargs"] = dict((k, v) for (k, v) in kwargs.iteritems() if self.is_valid_json_type(kwargs[k]))

                if self.track_request():
                    event_data = {"category": "dependency_start", "context":start_event, "timestamp" : time.time()}
                    if not self.aggregate_traces:
                        logger.info("dependency start", extra=event_data)
                    else:
                        self.thread_local.events.append(event_data)

                end_event = {"dependency_span_id" : remote_span_id,
                             "exception":False}
                try:
                    result = func(*args, **kwargs)
                    if log_return: end_event["response"] = str(result)
                    return result
                except Exception as ex:
                    end_event["exception"] = True
                    end_event["response"] = str(ex)
                    raise
                finally:
                    if self.track_request():
                        end_event = {"category": "dependency_end", "context":end_event, "timestamp" : time.time()}
                        if not self.aggregate_traces:
                            logger.info("dependency end", extra=end_event)
                        else:
                            self.thread_local.events.append(end_event)
            return inner
        return outer

    def finalize_request(self, status, response_headers=None, response_body=None,
                         exception_msg=None, traceback=None, return_span=False):
        try:
            if not getattr(self.thread_local, "initialized", False):
                return []

            tracking_id = self.thread_local.tracking_id
            span_id = self.thread_local.span_id

            if response_headers is None:
                response_headers = {}

            if exception_msg is not None:
                exception_msg = str(exception_msg)

            if traceback is not None:
                traceback = str(traceback)

            if response_body is not None:
                response_body = str(response_body)

            request_context = {
                "r_status": status,
                "r_headers" : response_headers,
                "r_body" : response_body,
                "r_exception" : {"msg" : exception_msg, "traceback" : traceback},
            }

            if self.track_request():
                event = {"category" : "request_end", "context" : request_context, "timestamp": time.time()}
                if not self.aggregate_traces:
                    logger.info("ending request", extra=event)
                else:
                    self.thread_local.events.append(event)
                    logger.info("completed request", extra={"category": "aggregated", "context": {
                        "events" : self.thread_local.events
                    }})

            self.thread_local.initialized = False
            response = [(self.tracking_id_header, str(tracking_id))]
            if return_span:
                response.append((self.span_id_header, str(span_id)))
            return response
        except Exception as ex:
            logger.exception("Failed to Finalize Request: %s" % ex)
            return []

    def get_tracking_info(self):
        tracking_id, span_id = None, None
        if hasattr(self.thread_local, "tracking_id"):
            tracking_id = self.thread_local.tracking_id

        if hasattr(self.thread_local, "span_id"):
            span_id = self.thread_local.span_id

        return {"tracking_id" : tracking_id, "span_id" : span_id}

    def is_valid_json_type(self, value):
        return isinstance(value, types.StringTypes) or isinstance(value, types.IntType) or isinstance(value, types.FloatType) or isinstance(value, types.LongType) or isinstance(value, types.BooleanType)

    def track_request(self):
        return self.enable_tracing and getattr(self.thread_local, "monitor_request", False)

    def get_remote_tracking_headers(self, as_dict=True):
        headers = []
        if hasattr(self.thread_local, "tracking_id"):
            headers.append((self.tracking_id_header, self.thread_local.tracking_id))
        if hasattr(self.thread_local, "remote_span_id"):
            headers.append((self.span_id_header, self.thread_local.remote_span_id))

        if not as_dict: return headers
        return dict([(k, v) for k, v in headers])


