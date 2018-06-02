import sys
from os.path import dirname, join
import logging

from deepspeech.model import Model
import scipy.io.wavfile as wav

logger = logging.getLogger('stream')


class Brain(object):

    def __init__(self, model, alphabet, num_features=26,
                 size_context=9, beam_width=500):
        self.model = model
        self.alphabet = alphabet

        logger.info('Loading Model')
        self.deepspeech = Model(self.model, num_features,
                                size_context, self.alphabet, beam_width)
        logger.info('Model loaded')

    def translate(self, wav_path):
        logger.info('translating...')
        fs, audio = wav.read(wav_path)
        return self.deepspeech.stt(audio, fs)

    def add_decoder(self, lm_path, trie_path, LM_W=1.75, WORD_COUNT_W=1.00, VALID_WORD_COUNT_W=1.00):
        self.deepspeech.enableDecoderWithLM(
            self.alphabet, lm_path, trie_path, LM_W, WORD_COUNT_W, VALID_WORD_COUNT_W)
        logger.info('Added decorder')
