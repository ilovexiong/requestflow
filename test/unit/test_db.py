import sys, logging, os
sys.path.append("../../src")
os.environ["HULU_ENV"] = "test"

import unittest, db, json, sys
import stubs

class TestDatabase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_stubs_zipkin_formatted_data(self):
        for stubname, data in stubs.GOOD_STUBS.items():
            error, lines = db.spec_test(data["raw_app_data"])
            self.assertIsNone(error)

            actual_formatted_data = db.get_zipkin_formatted(lines)
            expected_formatted_data = data["expected_zipkin_format"]

            if expected_formatted_data != actual_formatted_data:
                print "Raw Input: "
                print json.dumps(data["raw_app_data"], indent=4, sort_keys=True)

                print "Expected Output: "
                print json.dumps(expected_formatted_data, indent=4, sort_keys=True)

                print "Actual Output: "
                print json.dumps(actual_formatted_data, indent=4, sort_keys=True)

                print "Tested: %s" % stubname

            self.assertEquals(expected_formatted_data, actual_formatted_data)


    def test_stubs_raw_app_data_to_rendered(self):
        for stubname, data in stubs.GOOD_STUBS.items():
            error, lines = db.spec_test(data["raw_app_data"])
            self.assertIsNone(error)

            actual_formatted_data = db.get_hulu_formatted(lines)
            expected_formatted_data = data["expected_hulu_format"]

            if expected_formatted_data != actual_formatted_data:
                print "Raw Input: "
                print json.dumps(data["raw_app_data"], indent=4, sort_keys=True)

                print "Expected Output: "
                print json.dumps(expected_formatted_data, indent=4, sort_keys=True)

                print "Actual Output: "
                print json.dumps(actual_formatted_data, indent=4, sort_keys=True)

                print "Tested: %s" % stubname

            self.assertEquals(expected_formatted_data, actual_formatted_data)



if __name__ == "__main__":
    unittest.main()
