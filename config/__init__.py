from configparser import ConfigParser

from config.configuration import Config

config_parser = Config(ConfigParser(), ini_file='config/app.ini')
app_config_mapping_env = config_parser.get_map('AppConfig')
log_level = config_parser.get('LogConfig', 'log_level')
gh_token = config_parser.get('Github', 'gh_token')