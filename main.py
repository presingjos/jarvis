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

# Temporary entry point
if __name__ == '__main__':
    silent_remove('jarvis.log')
    silent_remove('output.wav')

    logging_config = join(
        dirname(__file__), 'src', 'logger_config.yaml')

    with open(logging_config) as stream:
        config = yaml.load(stream)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info('Log started')

    logger.info('Program start')

    model_path = join('models', 'output_graph.pb')
    alphabet_path = join('models', 'alphabet.txt')
    lm_path = join('models', 'lm.binary')
    trie_path = join('models', 'trie')

    jarvis = Jarvis(model_path, alphabet_path, lm_path, trie_path)
