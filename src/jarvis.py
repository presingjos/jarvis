import logging
import signal
import sys

import speech_recognition as sr
import yaml

from .common.check_internet_connection import have_internet
from .actions import Actions
from .errors import NoInternetConnectionError



class Jarvis():

    def __init__(self, keyword="jarvis", cache="cache.yaml", *args, **kwargs):
        # Check if we have a internet connection
        if not have_internet():
            raise NoInternetConnectionError()

        self.recognizer = sr.Recognizer()
        # For testing
        self.microphone = sr.Microphone()

        # Load the cache path
        self.cache_path = cache
        with open(self.cache_path) as stream:
            cache = yaml.load(stream)
        signal.signal(signal.SIGINT, self.dump_cache())

        # Load every single action
        self.actions = Actions(cache)

        logging.info("Adjusted for ambient noise: Quiet please")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while True:
            logging.info("You can start talking now")
            # with self.microphone as source:
            #     audio = self.recognizer.listen(source)
            try:
                # Look for a specific keyword
                # value = self.recognizer.recognize_sphinx(audio,
                #                                          keyword_entries=[(keyword, 0.8)])
                value = "jarvis"
            except sr.UnknownValueError:
                logging.info("Sorry did not catch that")
            else:
                self.actions.run("greeting")
                logging.info(f"Actively listening")

                while True:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source)
                    try:
                        value = self.recognizer.recognize_google(audio)
                        logging.info(f"I think you said: {value}")
                        if self.actions.run(value):
                            # To continue listening
                            pass
                        else:
                            break
                    except sr.UnknownValueError:
                        logging.info("mistakes were made")
                    except sr.RequestError as e:
                        logging.info(f"I got this error {e}")

    def dump_cache(self):

        def signal_handler(sig, frame):
            print("Dumping cache")
            with open(self.cache_path, 'w') as stream:
                yaml.dump(self.actions.cache, stream)
            sys.exit(0)

        return signal_handler