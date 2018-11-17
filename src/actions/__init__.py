import os
from os.path import dirname, join, splitext
import logging

from runpy import run_path

from ..errors import BuildError
from ..audio_files import Sayings

class Actions():

    def __init__(self, cache):
        self.audio_directory = join(dirname(__file__), "..", "audio_files")

        self._cache = cache
        self.sayings = Sayings()
        self.actions = {}

        # Loop through files in package and create any audio files
        # that do not exist
        for filename in os.listdir(dirname(__file__)):
            name, ext = splitext(filename)
            if ext == ".py" and name not in ["__init__"]:
                global_dict = run_path(join(dirname(__file__), filename))

                # Use a schema to validate the dictionary given
                if "SAYINGS" not in global_dict:
                    raise BuildError(
                        f"You need to define SAYINGS in {filename}"
                    )
                elif "ACTION_WORDS" not in global_dict:
                    raise BuildError(
                        f"You need to define ACTION_WORDS in {filename}"
                    )
                elif "action" not in global_dict:
                    raise BuildError(
                        f"You need to define an action function in {filename}"
                    )
                self.sayings.check(global_dict["SAYINGS"])

                action_word = global_dict["ACTION_WORDS"]
                if action_word in self.actions:
                    raise BuildError(
                        f"You've already specified {action_word}"
                    )
                self.actions[action_word] = global_dict["action"]

    def run(self, action_name):
        action_name = action_name.lower()
        for action in self.actions.keys():
            if action in action_name:
                logging.info(f"Running action associated with keyword {action}")
                self.actions[action](self)

    def say(self, saying):
        self.sayings.play(saying)

    def store(self, key, value):
        self._cache[key] = value
        logging.info(f"Storing {key}: {value}")

    def retrieve(self, key):
        try:
            result =  self._cache[key]
        except KeyError:
            result = None
        return result

    @property
    def cache(self):
        return self._cache