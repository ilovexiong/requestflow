#### Running Locally

	$ mkvirtualenv requestflow
	$ pip install -r requirements.txt
	$ python wsgi_[dev|test|stage|prod].py

#### Running Unit Tests

	$ nosetests test/unit

#### Running Acceptance Tests

	$ python test/integration/ba.py http://127.0.0.1:5000

