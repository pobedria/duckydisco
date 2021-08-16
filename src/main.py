#!/usr/bin/env python3
import threading

import numpy
import numpy as np
import pyaudio
import time

import librosa


from queue import Queue

from keyboard import keyboard

queue = Queue()


class AudioHandler:
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.stream = None

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  stream_callback=self.callback,
                                  input_device_index=6,
                                  frames_per_buffer=self.CHUNK)

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        n_fft = 8
        spectrum = librosa.stft(numpy_array, n_fft=n_fft, hop_length=n_fft//2)
        self.transform_spectrum(spectrum)
        return None, pyaudio.paContinue

    def transform_spectrum(self, spectrum):

        # Better change SQRT to LOG but now works and it is fine
        summa = numpy.sqrt(numpy.sqrt(numpy.sqrt(numpy.mean(np.abs(spectrum)**2, axis=1))))
        freq_list = summa
        new_list = []

        k = 20  # you can play with this coefficint to change bars aplitude on keyboard

        new_list.append(int(freq_list[0] * k))
        new_list.append(int(freq_list[1] * k))
        new_list.append(int(freq_list[2] * k))
        new_list.append(int(freq_list[3] * k))
        new_list.append(int(freq_list[4] * k))
        queue.put(new_list)

    def mainloop(self):
        while (self.stream.is_active()): # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            time.sleep(0.2)


def render_spectrum():
    with keyboard() as dev, dev.programming() as kb:
        seq = ['000000'] * (6 * 22 + 1)
        while True:
            freq_list = queue.get()
            new_seq = seq.copy()

            for i, fre in enumerate(freq_list):
                start = i
                end = start + 6 * fre
                for j in range(start, end+1, 6):
                    try:
                        if j == end:
                            new_seq[j] = "0000ff"
                        else:
                            new_seq[j] = "ff0000"
                    except IndexError:
                        pass
            kb.custom_mode(new_seq)


threading.Thread(target=render_spectrum).start()

audio = AudioHandler()
audio.start()     # open the the stream
audio.mainloop()  # main operations with librosa
audio.stop()