import os
from os.path import splitext, join, dirname
import hashlib
import base64

from playsound import playsound

from ..text_to_speech import create_mp3

class Sayings():

    def __init__(self):
        self._sayings = {}
        for filename in os.listdir(dirname(__file__)):
            name, ext = splitext(filename)
            if ext == ".mp3":
                self._sayings[name] = filename

    def check(self, sayings):
        for saying in sayings:
            hash_saying = self.hash_it(saying)
            if hash_saying not in self._sayings:
                file_name = create_mp3(saying, hash_saying)
                self._sayings[hash_saying] = file_name

    @staticmethod
    def hash_it(saying):
        saying = saying.lower().encode("utf-8")
        hasher = hashlib.sha1(saying)
        bin_string = base64.urlsafe_b64encode(hasher.digest()[:10])
        return bin_string.decode("ascii")

    def play(self, saying):
        hash_saying = self.hash_it(saying)
        try:
            file_name = self._sayings[hash_saying]
        except KeyError:
            file_name = create_mp3(saying, hash_saying)
            self._sayings[hash_saying] = file_name
        playsound(join(dirname(__file__), file_name))