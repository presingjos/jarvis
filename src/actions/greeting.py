from os.path import join, dirname

from playsound import playsound

ACTION_WORDS = "greeting"
SAYINGS = [
    "at your service, sir",
    "how can I be of service, sir",
    "yes, sir?"
]
def action(jarvis):
    jarvis.say(SAYINGS[0])
    return False
