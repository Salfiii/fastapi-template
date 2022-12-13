import configparser
import codecs
from app.helper.anonymize.Anonymize import Anonymize


class ConfigparserWrapper:
    """
    Readas a configuration file: https://docs.python.org/3/library/configparser.html
    Adds additional possibilieties like parsing the whole file as dict etc.
    """

    def __init__(self, path: str = None, config_string: str = None, **kwargs):
        """
        :param path: (str) path to the config-file
            HINT: if you have problems with paths, try this:
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "Config.ini")
        """
        # Parse the Config.ini
        self.configparser = configparser.ConfigParser(**kwargs)
        self.path = path
        if config_string:
            self.configparser.read_string(config_string)
        if path:
            self.configparser.read_file(codecs.open(self.path, "r", "utf8"))

    def get_dict(self) -> dict:
        """
        Returns the whole config file as a dict
        :return: dict
        """

        config = self.configparser
        sections_dict = dict()

        # get sections and iterate over each
        sections = config.sections()

        for section in sections:
            options = config.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = config.get(section, option)

            sections_dict[section] = temp_dict

        return sections_dict

    def get_dict_anon(self, exclude: list = ["pwd", "password", "secret"], wild_change: bool = True) -> dict:
        """
        :param exclude: (list[str], optional)
            List of possible values to exclude from the config-file.
            Defaults to ["pwd", "password", "secret"]
        :param wild_change: (bool, optional)
            If true; excludes values per wild-match, otherwise only if the match 100%.
            Defaults to True.
        :return: dict
        """

        conf_dict = self.get_dict()

        anon_conf = Anonymize(
            strip=exclude,
            hard_delete=False,
            overwrite_value=None,
            wild_change=wild_change
        ).perform_anonymization(conf_dict)

        return anon_conf
