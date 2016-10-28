The inspiration of this project is from zipkin twitter. Zipin is twitter open source implementations of google's distributed tracing system, Dapper. It
helps gather timing data needed to troubleshoot latency problems in microservice architectures. Our motivation is to integrate zipkin-ui with
requestflow backend server which will analyzes donki logs.

There are at least four important function of this project:

1.The ability to quickly troubleshoot why requests from a user are failing?
For example: Why is my video not playing?

2. The ability to better understand dependencies in our services?
For example: How many backend requests are made from a single playback call right now?

3. An additional way to understand where latency is consumed (dependency latency / network latency / application computation).
For example: Why are queries above the upper 99th percentile slow? This understanding can advise us on where queries can be optimized
(consider a multi get vs a set of sequential single gets).

4. A reliable way for teams to communicate when a request fails.

Currently teams communicate information such as user id and timestamp, but some services may not have user id in their logs and the timestamp may have multiple requests. By communicating in "X-Hulu-Request-Id" we can be certain we are analyzing the same request across different services. This includes CSA's who can forward this debug information to developers.


#### Running Locally

	$ mkvirtualenv requestflow
	$ pip install -r requirements.txt
	$ python wsgi_[dev|test|stage|prod].py

#### Running Unit Tests

	$ nosetests test/unit

#### Running Acceptance Tests

	$ python test/integration/ba.py http://127.0.0.1:5000
	
	
The demo can be seen here: https://youtu.be/GU8oKaDD2QE

