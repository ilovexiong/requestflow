import sys, logging, os
sys.path.append("../../src")
os.environ["HULU_ENV"] = "test"

from webtest import TestApp
from app import app
import unittest, mock

class TestApplication(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.db = mock.Mock()

        app.db_client = self.db
        self.test_app = TestApp(app)

    def test_health_check(self):
        resp = self.test_app.get("/health_check")
        self.assertEqual(200, resp.status_int)


if __name__ == "__main__":
    unittest.main()