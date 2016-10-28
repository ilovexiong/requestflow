import datetime
import time
from pythonjsonlogger import jsonlogger

class JsonLogFormatter(jsonlogger.JsonFormatter):
    def __init__(self, service_name, datacenter, env, hostname, get_tracking_info, *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, *args, **kwargs)
        self.service_name = service_name
        self.datacenter = datacenter
        self.env = env
        self.hostname = hostname
        self.get_tracking_info = get_tracking_info

    def add_fields(self, log_record, record, message_dict):
        message_dict = message_dict or {}
        message_dict["service_name"] = self.service_name
        tracking_info = self.get_tracking_info()
        message_dict["tracking_id"], message_dict["span_id"] = tracking_info["tracking_id"], tracking_info["span_id"]

        message_dict["environment"] = {
            "datacenter": self.datacenter,
            "name": self.env,
            "hostname": self.hostname,
        }

        message_dict["timestamp"] = time.time()
        message_dict["human_timestamp"] = datetime.datetime.now()

        if not hasattr(record, "category"):
            record.category = "application"

        jsonlogger.JsonFormatter.add_fields(self, log_record, record, message_dict)