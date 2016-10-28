import json
import logging
import re
import requests
import requestflow
from urlparse import urlparse
from config import track_stats, LOGSTASH_URL

logger = logging.getLogger(__name__)


class LogstashClient():
    def __init__(self, url):
        self.url = url
        self.SpanName=[]

    def __get_span_name(self,service_name):
        query = {"filter":{
            "bool":{
                "must":[
            {"term":{"donki_appname" : service_name}},
                    {"term":{"message": "tracking_id"}}]  #add an additional filter "tracking_id" to make the aggregation space small, can speed up a little
            }
        },
            "aggs": {
                "name": {
                    "terms": {
                        "field": "environment",
                        "size": 100
                    }
                }
            }
        }
        results = requests.get(self.url, data=json.dumps(query))
        raw_json = results.json()
        return raw_json

    def get_span_name(self,service_name):
        raw_data = self.__get_span_name(service_name)
        results = {}
        count = 0
        for entry in raw_data['aggregations']['name']['buckets']:
            if 'key' in entry:
                count += 1
                results[str(count)] = entry['key']
        return results

    def __get_service_name(self):
        query = {
            "filter": {
                "term": {"tag":"elasticsearch"}
            },
            "aggs": {
                "name": {
                    "terms": {
                        "field": "donki_appname",
                        "size": 1000
                    }
                }
            }
        }
        results = requests.get(self.url, data=json.dumps(query))
        raw_json = results.json()
        return raw_json


    def get_service_name(self):
        raw_data = self.__get_service_name()
        results={}
        count=0
        for entry in raw_data['aggregations']['name']['buckets']:
            if 'key' in entry:
                count+=1
                results[str(count)]=entry['key']
        return results



    @track_stats.timed("ResponseTimeByDependency.raw_logstash")
    def __get_raw(self, tracking_id,service_name,span_name,limit,start_time,end_time):
        if requestflow.tracking_id_not_valid(tracking_id):
            tracking_id="tracking_id"
        #query for tracking_id, if tracking_id="tracking_id" it query all the logs containing tracking-id information
        query_id= {"multi_match": {
                            "query": tracking_id,
                            "fields": ["base_message", "message"]
                        }
                    }
        #filtering according to service_name
        filter_service_name= {"term":{"donki_appname": service_name}}
        #filtering according to span_name for a given service_name
        filter_span_name= [{"term":{"donki_appname": service_name}},
                {"term":{"environment": span_name}}]

        # if time range is imported, we add it to the filter
        if start_time!=None and end_time!=None:
            time_range = {
                "range": {
                    "@timestamp": {
                        "lt": end_time,
                        "gt": start_time
                    }
                }
            }
            filter_service_name=[filter_service_name,time_range]
            filter_span_name.append(time_range)

        #limit here represent the number of logs we allow to return for each query, default 100
        if service_name=="all" or service_name == None:
            query = {"size":limit,
                    "query": query_id
            }
        elif span_name == "all" or span_name == None:
            query = {"size":limit,
                "query": {"filtered": {
                    "query": query_id,
                    "filter": {
                        "bool": {
                            "must": filter_service_name
                        }
                     }
                }
                }
            }
        else:
            query = {"size":limit,
                "query": {"filtered": {
                    "query": query_id,
                    "filter": {
                        "bool": {
                            "must": filter_span_name
                        }
                    }
                }
                }
            }

        results = requests.get(self.url, data=json.dumps(query))
        raw_json = results.json()
        return raw_json

    def get_raw(self, tracking_id,service_name="all",span_name="all",limit=100,start_time=None,end_time=None):
        raw_data = self.__get_raw(tracking_id,service_name,span_name,limit,start_time,end_time)
        results = []
        for entry in raw_data["hits"]["hits"]:
            source = entry["_source"]
            raw_msg = source["base_message"] if "base_message" in source else source["message"]
            try:
                body = json.loads(raw_msg)
            except:
                continue

            if "shipper_type" in source:
                body["environment"] = {
                    "name" : source["environment"],
                    "datacenter" : source["datacenter"],
                    "hostname" : source["hostname"],
                }
                body["category"] = "tracking_ignore"
            results.append(body)
        return results

    def __get_dependency(self, end_time, lookback):
        end_time=int(end_time)
        start_time= end_time- int(lookback)

        time_range={
            "range": {
                "@timestamp": {
                    "lt": end_time,
                    "gt": start_time
                }
            }
        }

        query_dependency={"multi_match": {
                    "query": "dependency_start",
                    "fields": ["base_message", "message"]
                }
                }
        # currently we get the dependency by querying all spans, we may need to change it with aggregation to make it faster
        # Since each query can only return one page, we set a big size to include all the information to save time
        query = {"size":1000,
            "query": {"filtered": {
                "query": query_dependency,
                "filter": time_range
            }
            }
        }

        results = requests.get(self.url, data=json.dumps(query))
        raw_json = results.json()

        return raw_json

    def get_dependency(self,end_time=1470435587914, lookback=864000000):
        raw_data = self.__get_dependency(end_time,lookback)
        results = []
        for entry in raw_data["hits"]["hits"]:
            source = entry["_source"]
            raw_msg = source["base_message"] if "base_message" in source else source["message"]
            try:
                body = json.loads(raw_msg)
            except:
                continue

            # The logs with shipper type will be categoried as tracking_ingore, and those logs will not be used in the analysis
            if "shipper_type" in source:
                body["environment"] = {
                    "name": source["environment"],
                    "datacenter": source["datacenter"],
                    "hostname": source["hostname"],
                }
                body["category"] = "tracking_ignore"
            results.append(body)
        return results




# Tests a blob of data and outputs the lines
def spec_test(raw_data):
    # Check each line can be converted to JSON
    inputs = []
    for i, line in enumerate(raw_data.split("\n")):
        if line.strip() == "": continue
        line = line.strip()
        try:
            processed = json.loads(line)
        except Exception as ex:
            return "Failure to JSON load line %s: %s" % (i+1, str(ex)), None

        inputs.append(processed)
    return json_spec_test(inputs)

def json_spec_test(inputs):
    # First check that all lines have span-id and tracking-id same at top level
    required_top_level_fields = [
        "tracking_id", "span_id",
        "timestamp", "service_name",
        "category"
    ]

    valid_categories = ["request_start", "dependency_start", "application", "dependency_end", "request_end", "aggregated"]

    for i, line in enumerate(inputs):
        if "category" not in line or line["category"] == "tracking_ignore":
            line["category"] = "tracking_ignore"
            continue

        for required in required_top_level_fields:
            if required not in line:
                return "%s field missing in line %s: %s" % (required, i+1, line), inputs

        if "context" not in line and line["category"] != "application":
            return "%s line is missing context field: %s" % (i+1, line), inputs

        if line["category"] not in valid_categories:
            return "Line %s doesn't have a valid category. Must be in %s: %s" % (i+1, valid_categories, line), inputs

        if line["category"] == "aggregated":
            if line["context"].keys() != ["events"]:
                return "Aggregated events should only have events inside context: %s - %s" % (i+1, line), inputs
            points = line["context"]["events"]
            for point in points:
                if "tracking_id" in point:
                    return "Unnecessary tracking_id in aggregated event line %s" % (i+1), inputs

                if "service_name" in point:
                    return "Unnecessary service_name in aggregated event line %s" % (i+1), inputs

                if "span_id" in point:
                    return "Unnecessary span_id in aggregated event line %s" % (i+1), inputs

                point["tracking_id"] = line["tracking_id"]
                point["span_id"] = line["span_id"]
                point["service_name"] = line["service_name"]

            res, new_inputs = json_spec_test(points)
            if res is not None:
                return res, new_inputs

        if "prod" in line["service_name"] or "stag" in line["service_name"]:
            return "Environment should not be in service name field", inputs

        if "dependency" in line["category"]:
            if "dependency_name" not in line["context"] and line["category"] == "dependency_start":
                return "Line %s doesn't have dependency_name in context: %s" % (i+1, line), inputs

            if "dependency_span_id" not in line["context"]:
                return "Line %s doesn't have dependency_span_id in context: %s" % (i+1, line), inputs

    #if len(inputs) > 1:
    #    base_span, base_tracking = inputs[0]["span_id"], inputs[0]["tracking_id"]
    #    for i, line in enumerate(inputs):
    #        if base_tracking != line["tracking_id"]:
    #            return "Tracking Id in line 1 is not the same as line %s: %s" % (i+1, line), inputs
    #
    #        if base_span != line["span_id"]:
    #            return "Span Id in line 1 is not the same as line %s: %s" % (i+1, line), inputs

    return None, inputs




def get_zipkin_formatted(raw_app_messages):
    app_messages = []
    for message in raw_app_messages:
        if message["category"] == "aggregated":
            for event in message["context"]["events"]:
                app_messages.append(event)
        else:
            app_messages.append(message)
    dependency_start_events = {}
    for message in app_messages:
        if message["category"] == "dependency_start":
            span_id = message["context"]["dependency_span_id"]
            name = message["context"]["dependency_name"]
            dependency_start_events[span_id] = name

    spans_to_annotations = {}
    def build_new_span_info(span, traceid, service_name):
        if span in spans_to_annotations: return
        spans_to_annotations[span] = {
            "traceId" : traceid,
            "name" : service_name,
            "id" : span,
            "binaryAnnotations" : [],
            "annotations" : [],

            # Fill these in after the fact
            "timestamp" : None,
            "duration" : None,
        }

    def set_timestamp_and_duration(ts, span):
        current_ts = spans_to_annotations[span]["timestamp"]
        current_duration = spans_to_annotations[span]["duration"]

        if current_ts is None:
            spans_to_annotations[span]["timestamp"] = ts
            spans_to_annotations[span]["duration"] = 0

        else:
            new_start_ts = min(current_ts, ts)
            spans_to_annotations[span]["timestamp"] = new_start_ts
            spans_to_annotations[span]["duration"] = max(current_duration, ts - new_start_ts)

    for i, msg in enumerate(app_messages):
        if msg["category"] == "tracking_ignore": continue

        trace_id = msg["tracking_id"]
        span_id = msg["span_id"]
        service_name = msg["service_name"]
        timestamp = int(msg["timestamp"] * 1000 * 1000)

        # Dependencies actually belong in the child span in zipkin
        if msg["category"] == "dependency_start":
            span_id = msg["context"]["dependency_span_id"]
            dependency_name = msg["context"]["dependency_name"]
            build_new_span_info(span_id, trace_id, dependency_name)

            event = {
                "timestamp": timestamp,
                "endpoint": {
                    "serviceName": service_name,
                    "ipv4": service_name,
                    "port": 0,
                },
                "value": "cs"
            }

            set_timestamp_and_duration(timestamp, span_id)
            spans_to_annotations[span_id]["annotations"].append(event)

        elif msg["category"] == "dependency_end":
            span_id = msg["context"]["dependency_span_id"]
            dependency_name = dependency_start_events[span_id]
            build_new_span_info(span_id, trace_id, dependency_name)

            event = {
                "timestamp": timestamp,
                "endpoint": {
                    "serviceName": service_name,
                    "ipv4": service_name,
                    "port": 0,
                },
                "value": "cr"
            }
            set_timestamp_and_duration(timestamp, span_id)
            spans_to_annotations[span_id]["annotations"].append(event)

        elif msg["category"] == "request_start":
            build_new_span_info(span_id, trace_id, service_name)

            event = {
                "timestamp": timestamp,
                "endpoint": {
                    "serviceName": service_name,
                    "ipv4": service_name,
                    "port": 0,
                },
                "value": "sr"
            }
            set_timestamp_and_duration(timestamp, span_id)
            spans_to_annotations[span_id]["annotations"].append(event)

            for key, value in msg["context"].items():
                event = {
                    "key": key,
                    "value": str(value),
                }
                spans_to_annotations[span_id]["binaryAnnotations"].append(event)

        elif msg["category"] == "request_end":
            build_new_span_info(span_id, trace_id, service_name)

            event = {
                "timestamp": timestamp,
                "endpoint": {
                    "serviceName": service_name,
                    "ipv4": service_name,
                    "port": 0,
                },
                "value": "ss"
            }
            set_timestamp_and_duration(timestamp, span_id)
            spans_to_annotations[span_id]["annotations"].append(event)

            for key, value in msg["context"].items():
                event = {
                    "key": key,
                    "value": str(json.dumps(value)),
                }
                if key=="r_body":
                    event = {
                        "key": key,
                        "value": str(value),
                    }
                spans_to_annotations[span_id]["binaryAnnotations"].append(event)

        elif msg["category"] == "application":
            build_new_span_info(span_id, trace_id, service_name)

            event = {
                "key" : "log_event_" + str(i),
                "value": str(msg["message"]),
            }

            set_timestamp_and_duration(timestamp, span_id)

            spans_to_annotations[span_id]["binaryAnnotations"].append(event)

    return sorted(spans_to_annotations.values(), key=lambda x: x["timestamp"])


def get_dependency_formatted(raw_app_messages):
    app_messages = []
    for message in raw_app_messages:
        if message["category"] == "aggregated":
            for event in message["context"]["events"]:
                app_messages.append(event)
        else:
            app_messages.append(message)
    dependency_mapping = {}
    for msg in app_messages:
        service_name = msg["service_name"]
        if msg["category"] == "dependency_start":
            dependency_name = msg["context"]["dependency_name"]
            if service_name not in dependency_mapping:
                dependency_mapping[service_name] = {}
            if dependency_name not in dependency_mapping[service_name]:
                dependency_mapping[service_name][dependency_name]=1
            else:
                dependency_mapping[service_name][dependency_name]+=1

    dependency_link=[]
    for service_name in dependency_mapping:
        for dependency_name in dependency_mapping[service_name]:
            dependency_link.append({"parent":service_name,
                                 "child":dependency_name,
                                 "callCount":dependency_mapping[service_name][dependency_name]
            })
    return dependency_link

def get_hulu_formatted(raw_app_messages):
    app_messages = []
    for message in raw_app_messages:
        if message["category"] == "aggregated":
            for event in message["context"]["events"]:
                event["tracking_id"] = event["tracking_id"]
                event["span_id"] = event["span_id"]
                event["service_name"] = event["service_name"]
                app_messages.append(event)
        else:
            app_messages.append(message)


    unsorted_request_spans = {}
    unsorted_dependency_spans = {}

    dependency_mapping = {}
    main_mapping = {}
    for msg in app_messages:
        if msg["category"] == "dependency_start" or msg["category"] == "dependency_end":
            span = msg["context"]["dependency_span_id"]
            if span not in dependency_mapping:
                dependency_mapping[span] = {}

            dependency_mapping[span][msg["category"]] = msg
            if "dependency_start" in dependency_mapping[span] and "dependency_end" in dependency_mapping[span]:
                s = dependency_mapping[span]["dependency_start"]
                e = dependency_mapping[span]["dependency_end"]
                label = "%s dependency call" % (s["service_name"])
                time = {
                    "starting_time" : int(1000*s["timestamp"]),
                    "ending_time" : int(1000*e["timestamp"]),
                    "label" : s["context"]["dependency_name"] + " | " + str(1000*(e["timestamp"] - s["timestamp"]))[:5] + " ms"
                }

                if time["ending_time"] == time["starting_time"]:
                    time["ending_time"] += 1

                if span not in unsorted_dependency_spans:
                    unsorted_dependency_spans[span] = {"label" : label, "times" : []}
                unsorted_dependency_spans[span]["times"].append(time)

        elif msg["category"] == "request_start" or msg["category"] == "request_end":
            span = msg["span_id"]
            if span not in main_mapping:
                main_mapping[span] = {}

            main_mapping[span][msg["category"]] = msg
            if "request_start" in main_mapping[span] and "request_end" in main_mapping[span]:
                s = main_mapping[span]["request_start"]
                e = main_mapping[span]["request_end"]
                label = "%s application call" % (s["service_name"])
                time = {
                    "starting_time" : int(1000*s["timestamp"]),
                    "ending_time" : int(1000*e["timestamp"]),
                    "label" : str(1000*(e["timestamp"] - s["timestamp"]))[:5] + " ms"
                }

                if time["ending_time"] == time["starting_time"]:
                    time["ending_time"] += 1

                unsorted_request_spans[span] = {"label" : label, "times" : [time]}
    return unsorted_request_spans.values() + unsorted_dependency_spans.values()

def get_basic_client():
    return LogstashClient(LOGSTASH_URL)
