import os
import errno
from os.path import join, dirname
import logging
import logging.config

import yaml

from src.jarvis import Jarvis


def silent_remove(file_path):
    try:
        os.remove(file_path)
    except OSError as err:
        if err.errno != errno.ENOENT:
            raise


# Main entry point
if __name__ == "__main__":
    silent_remove("jarvis.log")
    silent_remove("output.wav")

    # Set up the logger
    logging_config = join(
        dirname(__file__), "logger_config.yaml")
    with open(logging_config) as stream:
        config = yaml.load(stream)
    logging.config.dictConfig(config)
    logging.info("Log started")
    logging.info("Program start")

    logging.info("")
    with open(join(dirname(__file__), "setup.yaml")) as stream:
        setup = yaml.load(stream)

    # Start up Jarvis
    jarvis = Jarvis(**setup)
