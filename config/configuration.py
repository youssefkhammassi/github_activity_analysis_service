import os
from configparser import ConfigParser


class Config:
    """
    A class used to generate an environment variable for LELY project
    """
    ENV_VAR_PREFIX_NAME = 'LELY_'
    DEFAULT_SEPARATOR = '_'

    def __init__(self, config_parser: ConfigParser, ini_file: str = None):
        """
        :param config_parser: instance of class to read & write configuration files (INI files)
        """
        #Fetch env vars passed in the helm chart that start with MIRA_
        self.env_var = dict(filter(lambda item: item[0].startswith(self.ENV_VAR_PREFIX_NAME), os.environ.items()))
        if ini_file is None:
            config_parser.read('config/app.ini')
        else:
            config_parser.read(ini_file)
        self.config_file_var = {s: dict(config_parser.items(s)) for s in config_parser.sections()}

    def prepare_env_var_name(self, variable):
        """
        Prepare env. variables that are in INI files
        :param variable: environment variable to be created
        :return: Environment variable
        """
        return variable.replace('-', self.DEFAULT_SEPARATOR).replace('.', self.DEFAULT_SEPARATOR).upper()

    def get(self, section, variable):
        """
        Get the value of the env. variable
        :param section: header which contains keys and values
        :param variable: env. variable key
        :return: A string
        """
        env_var_key = self.ENV_VAR_PREFIX_NAME + self.prepare_env_var_name(
            section) + self.DEFAULT_SEPARATOR + self.prepare_env_var_name(variable)
        if env_var_key in self.env_var:
            return self.env_var.get(env_var_key)
        else:
            return self.config_file_var[section][variable]

    def get_map(self, section) -> dict:
        """
        Get the values of all the env. variables of a section
        :param section: header which contains keys and values
        :return: A dict
        """
        env_vars = self.config_file_var[section].keys()
        config_map = {}
        for element in env_vars:
            config_map[element] = self.get(section, element)
        return config_map
