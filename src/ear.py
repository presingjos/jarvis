import logging

import pyaudio
import wave

logger = logging.getLogger('stream')


class Ear(object):

    def __init__(self, format, channel, rate, input, frames_per_buffer):

        self.p = pyaudio.PyAudio()
        self.format = format
        self.channel = channel
        self.rate = rate
        self.input = input
        self.frames_per_buffer = frames_per_buffer
        self.wave_output_filename = 'output.wav'
        self.record_time = 5

        self.frames = []

    def listen(self):
        self.stream = self.p.open(format=self.format,
                                  channels=self.channel,
                                  rate=self.rate,
                                  input=self.input,
                                  frames_per_buffer=self.frames_per_buffer)
        logger.info('Starting to record')
        for i in range(0, int(self.rate / self.frames_per_buffer * self.record_time)):
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

    def stop_listen(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        logger.info('Stopped recording')

        # TODO: Remove this and just pass frames to model for
        # translation
        wf = wave.open(self.wave_output_filename, 'wb')
        wf.setnchannels(self.channel)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        logger.info('Writing to jarvis.log')
        return self.wave_output_filename

if __name__ == '__main__':

    # Intialize an ear
    params = {
        'format': pyaudio.paInt16,
        'channel': 1,
        'rate': 16000,
        'input': True,
        'frames_per_buffer': 1024
    }

    ear = Ear(**params)
    ear.listen()
    ear.stop_listen()
