import os
from os.path import dirname, join

from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Jarvis-444675c15f5a.json"

def create_mp3(saying, file_name):
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=saying)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name="en-AU-Wavenet-B",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    file_path = join(dirname(__file__), "audio_files", file_name+".mp3")
    with open(file_path, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    return file_name+".mp3"