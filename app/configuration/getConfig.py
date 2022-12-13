import os
import warnings
from app.configuration.configparser.wrapper import ConfigparserWrapper as ConfigParser
from app.helper.log.logger import Logger
from app.helper.pattern.singleton import Singleton


class Config(metaclass=Singleton):
    """
    Get the configuration.ini and the source connection.
    """

    def __init__(self):
        # Parse the Config.ini
        self.config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini")
        self.config = ConfigParser(self.config_path)
        self.configparser = self.config.configparser

        try:
            self.is_local = True if os.environ["IS_LOCAL"].upper().strip() == "TRUE" else False
            print("IS_LOCAL: " + str(self.is_local))
        except Exception as e:
            warnings.warn(str(e))
            self.is_local = False
        self.API_ID: int = self.configparser["API"]["ID"]
        try:
            api_version_file_path = "./version.txt"
            api_version_file_path = "." + api_version_file_path if self.is_local else api_version_file_path
            with open(api_version_file_path, "r") as file:
                self.API_VERSION = file.read()
        except Exception as e:
            warnings.warn(str(e))
            self.API_VERSION: str = "UNKNOWN"
        self.configparser["API"]["VERSION"] = self.API_VERSION
        self.logger = Logger(self.API_ID, Logger.SINK.STDOUT)

        try:
            self.debug = False if self.configparser["API"]["DEBUG"].upper().strip() == "FALSE" else True
            print("Debug mode : " + str(self.debug))
        except Exception as e:
            warnings.warn(str(e))
            self.debug = True

        try:
            self.in_folder: str = "." + self.configparser["FOLDER"]["IN"] if self.is_local \
                else self.configparser["FOLDER"]["IN"]
            self.out_folder: str = "." + self.configparser["FOLDER"]["OUT"] if self.is_local \
                else self.configparser["FOLDER"]["OUT"]
            self.test_folder: str = "." + self.configparser["FOLDER"]["TEST"] if self.is_local \
                else self.configparser["FOLDER"]["TEST"]
            self.cache_folder: str = "." + self.configparser["FOLDER"]["CACHE"] if self.is_local \
                else self.configparser["FOLDER"]["CACHE"]

        except Exception as e:
            self.logger.log(self.logger.LEVEL.ERROR, 500, "Could not parse the config: " + str(e),
                            "app.configuration.getConfig.Config")

        self.configuration_dict = self.config.get_dict_anon(exclude=["pwd", "password", "secret", "url"])
        print("CONFIGURATION: (Some key/value pairs are anonymized or not present due to sensitive data)")
        print(self.configuration_dict)
