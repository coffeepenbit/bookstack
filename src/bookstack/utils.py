import logging

import yaml


def configure_loggers(loglevel, logger, logging_format):
    formatter = logging.Formatter(logging_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(loglevel)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(loglevel)


def get_conf(conf_filepath):
    try:
        with open(conf_filepath, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file was not found at: \"{conf_filepath}.\""
        )
