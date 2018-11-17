# Tell me when to run the function
ACTION_WORDS = "marcus"

# Tell me what to say
SAYINGS = [
    "Hi Marcus, I will see you at Thanksgiving!"
]

def action(jarvis):
    jarvis.say(SAYINGS[0])
    return False