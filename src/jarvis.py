from os.path import join, dirname

import logging
import logging.config
import pyaudio

from .ear import Ear
from .brain import Brain


logger = logging.getLogger(__name__)


class Jarvis(object):

    def __init__(self, model_path, alphabet_path, lm_path=None, trie_path=None):

        logger.info('Importing model')
        self.brain = Brain(model_path, alphabet_path)

        if lm_path and trie_path:
            self.brain.add_decoder(lm_path, trie_path)

        self.ear_args = {
            'format': pyaudio.paInt16,
            'channel': 1,
            'rate': 16000,
            'input': True,
            'frames_per_buffer': 1024
        }
        self.ear = Ear(**self.ear_args)
        self.ear.listen()
        translation = self.brain.translate(self.ear.stop_listen())

        print(translation)
