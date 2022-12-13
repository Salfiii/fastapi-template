import json
from datetime import datetime
from dataclasses import asdict
from pydantic.dataclasses import dataclass


@dataclass
class Log:
    timestamp: str
    api_id: int
    level: int
    status_code: int
    message: str = None
    traceback: str = None
    path: str = None
    user: str = None
    uuid: str = None
    trace_id: str = None

    def __init__(self, timestamp: datetime, api_id: int, level: int, status_code: int, message: str,
                 traceback: str, path: str, user: str, uuid: str, trace_id: str, treat_all_args_as_string: bool = False):
        """

        :param timestamp:
        :param api_id:
        :param level:
        :param status_code:
        :param message:
        :param traceback:
        :param path:
        :param user:
        :param uuid:
        :param trace_id:
        """
        self.timestamp = timestamp.isoformat()
        self.api_id = str(api_id) if treat_all_args_as_string else api_id
        self.level = str(level) if treat_all_args_as_string else level
        self.status_code = str(status_code) if treat_all_args_as_string else status_code
        self.message = message
        self.traceback = traceback
        self.path = path
        self.user = user
        self.uuid = uuid
        self.trace_id = trace_id

    def to_json_string(self) -> str:
        """
        Return the dataclass as a json string
        :return: (str) json-string representation of the log dataclass
        """
        return json.dumps(asdict(self))

    def to_dict(self) -> dict:
        """
        Return the dataclass as a dict
        :return:
        """
        return asdict(self)
