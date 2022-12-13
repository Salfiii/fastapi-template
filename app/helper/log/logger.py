from __future__ import print_function

import json
import sys
import traceback
import warnings
from datetime import datetime
from enum import Enum

from pymongo import MongoClient

from app.helper.log.log import Log


class Logger:
    class SINK(Enum):
        STDOUT = 0
        FILE = 1
        MONGODB = 2

    class LEVEL(Enum):
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 99

    class MODE(Enum):
        ERROR = 0
        WARNING = 1
        INFO = 2
        DEBUG = 3

    def __init__(self, api_id: int, sink: SINK = SINK.STDOUT, uid: str = None, pwd: str = None, mode: MODE = MODE.INFO,
                 file_path: str = "./log.txt",
                 mongodb_url: str = "mongodb://{UID}:{PWD}@{HOST}/?authSource=database",
                 mongodb_db: str = None, mongodb_collection: str = None, mongodb_host: str = None,
                 treat_all_args_as_string: bool = False
                 ):
        """
        APIKEY auth.-provider for python webservices
        :param api_id: (int) API Identificator
        :param sink: (SINK) How should be logged?
        :param uid: (str) user
        :param pwd: (str) password
        :param mode: (MODE) Logging mode, decides which logs should be forwarded/printed
        :param file_path: If the sink type "FILE" is used, you can specify the path to the file.
        :param mongodb_url: Provide a mongodb url in the specified format: https://docs.mongodb.com/manual/reference/connection-string/
            If you specify the parameters "uid" and "pwd", please us the following format "mongodb://{UID}:{PWD}@{HOST}/?authSource=database" and user and password will be replaced with the actual values.
        :param mongodb_db: MongoDB database where the collection of the logs can be found
        :param mongodb_collection: MongoDB collection where the logs should be stored
        :param mongodb_host: MongoDB Host URL
        :param treat_all_args_as_string: if True, converts all given arguments as app_id, error_code etc. to string
            (Useful for kibana logging over OKD where a central parser is in place which only uses strings!)
        """
        self.sink = sink
        self.api_id: int = api_id
        self.mode = mode
        self.treat_all_args_as_string = treat_all_args_as_string
        if sink == self.SINK.FILE:
            self.file_handle = open(file_path, "a+")
        if sink == self.SINK.MONGODB:
            if uid and pwd and mongodb_host:
                self.__mongodb_url = mongodb_url.replace("{UID}", uid).replace("{PWD}", pwd).replace("{URL}", mongodb_host)
            else:
                self.__mongodb_url = mongodb_url
            self.mongo_client = MongoClient(self.__mongodb_url)
            self.mongodb_collection = self.mongo_client[mongodb_db][mongodb_collection]

    def print_err(*args, **kwargs):
        """
        Print to stderr instead regular stdout
        :param args:
        :param kwargs:
        :return:
        """
        print(*args, file=sys.stderr, **kwargs)

    def log(self, level: LEVEL, status_code: int, message: str = "", path: str = "", user: str = "", uuid: str = "",
            trace_id: str = "") -> (bool, Log):
        """
        :param level: Log-Level 0 = INFO, 1 = WARNING, 99 = ERROR
        :param status_code: HTTP-Status Code
        :param message: Log message
        :param path: Path/URL to the method that created the log
        :param user: user wo called the api
        :param uuid: unique identifier of the current run
        :param trace_id: trace id of the current run/object which can/should be sent to the precending task.
        :return: [bool] insert/print status of the log
        """

        ts = datetime.now()
        tb = traceback.format_exc() if level == self.LEVEL.ERROR else ""

        _log = Log(
            ts,
            self.api_id,
            level.value,
            status_code,
            message,
            tb,
            path,
            user,
            uuid,
            trace_id,
            self.treat_all_args_as_string
        )
        # STDOUT - is always used according to mode
        if level == self.LEVEL.ERROR and self.mode.value >= 0:
            self.print_err(_log.to_json_string())

        if level == self.LEVEL.WARNING and self.mode.value > 0:
            warnings.warn(_log.to_json_string())

        # normal print, always except for debug
        if level == self.LEVEL.INFO:
            print(_log.to_json_string())

        # only print debugs if the mode is set to DEBUG and LEVEL is Debug
        if level == self.LEVEL.DEBUG and self.mode == self.MODE.DEBUG:
            print(_log.to_json_string())

        success = True
        # other log implementations

        if self.sink == self.SINK.FILE:
            success = self.__log_file(_log)
        elif self.sink == self.SINK.MONGODB:
            success = self.__log_mongodb(_log)
        return success, _log


    def __log_file(self, log: Log) -> bool:
        """
        Write log to a txt file
        """
        success = False
        try:
            self.file_handle.write(json.dumps(log.to_json_string(), indent=4, ensure_ascii=False) + "\n")
            success = True
        except Exception as e:
            pass
        return success

    def __log_mongodb(self, log: Log) -> bool:
        """
        Write log to a txt file
        """
        success = False
        try:
            log_dict = log.to_dict()
            result = self.mongodb_collection.insert_one(log_dict)
            id = result.inserted_id
            success = True
        except Exception as e:
            pass
        return success
