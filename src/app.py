import json
import re
from flask import request, make_response, render_template, jsonify
from flask import Flask
from flask import Response

from config import setup_logging, track_stats, setup_sso
from hpc.sso.flask_client import exempt_from_sso

import logging
import sys
import traceback
import db

setup_logging()
app = Flask(__name__)
app.debug = True
app.db = db.get_basic_client()

hulu_sso = setup_sso(app)

logger = logging.getLogger(__name__)



@app.route('/')
@track_stats.timed("ResponseTimeByEndpoint.index")
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
@track_stats.timed("ResponseTimeByEndpoint.static_proxy")
def static_proxy(path):
    return app.send_static_file(path)



@app.route("/health_check")
@exempt_from_sso
@track_stats.timed("ResponseTimeByEndpoint.health_check")
def health_check():
    return Response("OK", content_type="text/plain")




### Your Business Logic ###




@app.route("/render_traces_bulk", methods=["POST"])
@track_stats.timed("ResponseTimeByEndpoint.render_traces_bulk")
def render_traces_bulk():
    form = request.form["traces"]
    error, traces = db.spec_test(form)
    if error is not None:
        return jsonify({"status" : "error", "message" : error})
    hulu_trace = db.get_hulu_formatted(traces)
    return jsonify({ "status" : "success", "message" : hulu_trace })

@app.route("/render_live_trace", methods=["POST"])
@track_stats.timed("ResponseTimeByEndpoint.render_live_trace")
def render_live_trace():
    tracking_id = request.form["tracking_id"]
    raw_traces = app.db.get_raw(tracking_id)
    error, traces = db.json_spec_test(raw_traces)
    if error is not None:
        return jsonify({"status" : "error", "message" : error})
    hulu_trace = db.get_hulu_formatted(traces)
    return jsonify({ "status" : "success", "message" : hulu_trace })

@app.route("/validate_traces/<traceId>")
@track_stats.timed("ResponseTimeByEndpoint.validate_traces")
def validate_traces(traceId):
    raw_traces = app.db.get_raw(traceId)
    error, traces = db.json_spec_test(raw_traces)
    return jsonify({"error" : error, "traces" : traces, "raw_traces": raw_traces})

@app.route("/es_raw_trace/<traceId>")
@track_stats.timed("ResponseTimeByEndpoint.hulu_es_trace")
def es_raw_trace(traceId):
    raw_traces = app.db.get_raw(traceId)
    return jsonify({"raw_traces" : raw_traces})

@app.route("/hulu_raw_trace/<traceId>")
@track_stats.timed("ResponseTimeByEndpoint.hulu_raw_trace")
def hulu_raw_trace(traceId):
    raw_traces = app.db.get_raw(traceId)
    error, traces = db.json_spec_test(raw_traces)
    if error is not None:
        return jsonify({"status" : "error", "message" : error})
    hulu_trace = db.get_hulu_formatted(traces)
    return jsonify({ "status" : "success", "message" : hulu_trace })


@app.route("/zipkin_raw_trace/<traceId>")
@track_stats.timed("ResponseTimeByEndpoint.zipkin_raw_trace")
def zipkin_raw_trace(traceId):
    raw_traces = app.db.get_raw(traceId)
    error, traces = db.spec_test(raw_traces)
    if error is not None:
        return jsonify({"status" : "error", "message" : error})
    zipkin_trace = db.get_zipkin_formatted(traces)
    return jsonify({ "status" : "success", "message" : zipkin_trace })

### Things Related to Zipkin ###
@app.route('/config.json',methods=['GET'])
@exempt_from_sso
@track_stats.timed("ResponseTimeByEndpoint.setconfig")
def setconfig():
    return jsonify({})

DEMO=True
@app.route('/api/v1/services',methods=['GET'])
@exempt_from_sso
@track_stats.timed("ResponseTimeByEndpoint.get_services")
def get_services():
    if DEMO: #TODO, the ELS currectly takes a long time to query all service_names, for demo purpose, we only include "banya", "deejay","geok", they will be removed later
        return jsonify({"1":"banya","2":"deejay","3":"geok"})
    hulu_service_name=app.db.get_service_name()
    return jsonify(hulu_service_name)

@app.route('/api/v1/spans')
@exempt_from_sso
@track_stats.timed("ResponseTimeByEndpoint.get_spans")
def get_spans():
    service_name=request.args.get('serviceName')
    span_name=app.db.get_span_name(service_name)
    return jsonify(span_name)

@app.route('/api/v1/dependencies')
@exempt_from_sso
def get_dependency():
    defaultlookback=86400000
    # end_time means the end of the time period in searching (unit: millisecond)
    end_time=request.args.get('endTs')
    # lookback means the length between the start time and end time in searching (unit: millisecond)
    lookback=request.args.get('lookback')
    if lookback==None:
        lookback=defaultlookback
    raw_traces=app.db.get_dependency(end_time,lookback)
    error, traces = db.json_spec_test(raw_traces)
    if error is not None:
        return jsonify({"status": "error", "message": error})
    dependency_link = db.get_dependency_formatted(traces)
    return json.dumps(dependency_link)


@app.route('/api/v1/traces')
@exempt_from_sso
def query_traces():
    trace_id=request.args.get('annotationQuery')
    service_name=request.args.get('serviceName')
    span_name = request.args.get('spanName')
    limit=request.args.get('limit')
    end_time=request.args.get('endTs')
    lookback=request.args.get('lookback')
    start_time=int(end_time)-int(lookback)
    raw_traces = app.db.get_raw(trace_id,service_name,span_name,limit,start_time,end_time)
    error, traces = db.json_spec_test(raw_traces)
    if error is not None:
        return jsonify({"status": "error", "message": error})
    zipkin_trace = db.get_zipkin_formatted(traces)
    collect_trace={}
    for item in zipkin_trace:
        trace_id=item['traceId']
        if trace_id == None:
            continue
        if trace_id not in collect_trace:
            collect_trace[trace_id]=[]
        collect_trace[trace_id].append(item)
    return json.dumps(collect_trace.values())

DEBUG=False
@app.route("/api/v1/trace/<trace_id>")
@exempt_from_sso
def zipkin_trace(trace_id):
    if DEBUG:
        raw_traces = '''
{"process": 27851, "levelname": "INFO", "name": "banya", "message": "user_view_count user_id: 2000086331, device: 1, playlist_device: 73, views_count: 0, client_ip_num: 3495664710, device_id: 1BDF1C345E033F0C79056F7E7D6F5E5E, add_block: None, add_is_extra_multi_view: False, total_views_count: 0", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.674196, "span_id": "1", "category": "application"}
{"process": 27851, "levelname": "STATS", "name": "banya", "message": "adding view {'hits.token': 'tM3KIRQc', '_id': 2000086331}", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.674438, "span_id": "1", "category": "application"}
{"process": 27851, "levelname": "INFO", "name": "src.tracking_id", "message": "completed request", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.677775, "span_id": "1", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1458016928.630059, "context": {"body": {"rv": "790906", "guid": "1BDF1C345E033F0C79056F7E7D6F5E5E", "kv": "16875", "language": "en"}, "headers": {}, "url_full": "http://banya.staging.hulu.com/banya_playlist?vp=1&video_id=50153632&skip_ad_support=true&region=US&version=1&dp_id=hulu&pp=hulu&device_id=1BDF1C345E033F0C79056F7E7D6F5E5E&ad_ui_capable=true&device=73&x_redirect_header=X-Accel-Redirect&x_redirect=%2Fplaylist_end_track", "url_args": {}, "http_method": "POST", "url_host": "banya.staging.hulu.com", "url_path": "/banya_playlist"}}, {"category": "dependency_start", "timestamp": 1458016928.650321, "context": {"dependency_span_id": "1.1", "args": ["GET", "/user/2000086331"], "dependency_name": "kardashian", "kwargs": {}, "function_name": "_make_request"}}, {"category": "dependency_end", "timestamp": 1458016928.655745, "context": {"exception": false, "dependency_span_id": "1.1"}}, {"category": "dependency_start", "timestamp": 1458016928.663873, "context": {"dependency_span_id": "1.2", "args": ["GET", "/ip2geoinfo"], "dependency_name": "geok", "kwargs": {}, "function_name": "_make_request"}}, {"category": "dependency_end", "timestamp": 1458016928.669962, "context": {"exception": false, "dependency_span_id": "1.2"}}, {"category": "request_end", "timestamp": 1458016928.677702, "context": {"r_headers": {"X-Accel-Redirect": "/playlist_end_track?vp=1&package_id=2", "Content-type": "text/plain"}, "r_body": "OK", "r_exception": {"msg": null, "traceback": null}, "r_status": "200 OK"}}]}}
{"process": 24445, "levelname": "INFO", "name": "src.server.tracking_id", "message": "completed request", "service_name": "geok", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "stage"}, "human_timestamp": "2016-03-14 21:42:08", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.668461, "span_id": "1.2", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1458016928.667579, "context": {"body": {}, "headers": {}, "url_full": "http://geok.els.staging.hulu.com/ip2geoinfo?ip=208.91.156.70&no_override=0&preferred_country=US&format=json", "url_args": {}, "http_method": "GET", "url_host": "geok.els.staging.hulu.com", "url_path": "/ip2geoinfo"}}, {"category": "request_end", "timestamp": 1458016928.668326, "context": {"r_headers": {"Content-type": "application/json"}, "r_body": "", "r_exception": {"msg": null, "traceback": null}, "r_status": "200 OK"}}]}}
'''
        error, traces = db.spec_test(raw_traces)
    else:
        raw_traces = app.db.get_raw(trace_id)
        error, traces = db.json_spec_test(raw_traces)

    if error is not None:
        return jsonify({"status" : "error", "message" : error})
    zipkin_trace = db.get_zipkin_formatted(traces)
    return json.dumps(zipkin_trace)


### Necessary Flask Setup ###

from hpc.requeststore import setup_tracking_id, get_tracking_id, set_trace

@app.before_request
def before_request():
    setup_tracking_id(request.headers.get('Tracking-Id', None))

@app.errorhandler(Exception)
def handle_exception(ex):
    logger.exception("Unhandled Exception: %s" % ex)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    rendered = "\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback, limit=50))
    return make_response(rendered, 500, {'Content-Type': 'text/plain'})
    
@app.after_request
def apply_tracking_id(response):
    response.headers["Tracking-ID"] = get_tracking_id()
    return response

### Debugging Endpoints ###

@app.route("/test_fail")
@track_stats.timed("ResponseTimeByEndpoint.test_fail")
@exempt_from_sso
def test_fail():
    raise Exception("manual-fail-test")

@app.route("/test_environ_logging")
@track_stats.timed("ResponseTimeByEndpoint.test_environ_logging")
@exempt_from_sso
def test_environ_logging():
    set_trace({"user_id" : 1, "value" : 2})
    logger.error("Test Logging Environ")
    return Response("OK", content_type="text/plain")
