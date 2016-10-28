import sys,os,cherrypy
sys.path.append("../.")

import unittest
import requestflow

class TestTracer(unittest.TestCase):
    def deejay_output(self,request):
    # Given a request, return the tracking-Id by tracer
        tracer = requestflow.Tracer(service_name='deejay', aggregate_traces=True, enable_tracing=False, environment='dev', datacenter='els')
        status = "200 OK"
        tracer.initialize_request(request)
        return tracer.finalize_request(status)

    def test_no_tracking_id(self):
    # if there is no tracking-id information in request, the tracer should return a generated tracking-id, and the tracking-id should be legal
        request = cherrypy.request
        request.headers = {}
        self.assertFalse(requestflow.tracking_id_not_valid(self.deejay_output(request)[0][1]))


    def test_tracking_id(self):
    # if there is tracking-id information in request, the tracer should return the tracking-id
        request = cherrypy.request
        request.headers = {
            "X-Hulu-Tracking-Id": "06ce9756f7f85938a0707eac814d467a"
        }
        good_tracing = [('X-Hulu-Tracking-Id', '06ce9756f7f85938a0707eac814d467a')]
        self.assertEquals(self.deejay_output(request),good_tracing)



if __name__=="__main__":
    unittest.main()

