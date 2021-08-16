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

        # D = librosa.amplitude_to_db(np.abs(spectrum), ref=np.max)
        summa = numpy.sqrt(numpy.sqrt(numpy.sqrt(numpy.mean(np.abs(spectrum)**2, axis=1))))
        freq_list = summa
        new_list = []

        # sys.stdout.write("\r")
        # for i, freq in enumerate(freq_list):
        #     sys.stdout.write(f"{freq:16.8}\t")
        # sys.stdout.flush()

        K = 20
        # new_list.append(int(freq_list[0] * K * 22/22) -5)
        # new_list.append(int(freq_list[1] * K * 22/19) -5)
        # new_list.append(int(freq_list[2] * K * 22/13) -5)
        # new_list.append(int(freq_list[3] * K * 22/12) -5)
        # new_list.append(int(freq_list[4] * K * 22/11) -5)

        new_list.append(int(freq_list[0] * K ))
        new_list.append(int(freq_list[1] * K ))
        new_list.append(int(freq_list[2] * K ))
        new_list.append(int(freq_list[3] * K ))
        new_list.append(int(freq_list[4] * K ))

        # render_spectrum(new_list)
        queue.put(new_list)


    def mainloop(self):
        while (self.stream.is_active()): # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            time.sleep(0.2)

max_amplitude = [0] * 5
count = 5
def render_spectrum():

    global max_amplitude
    global count
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
                            # if j > max_amplitude[i]:
                            new_seq[j] = "0000ff"
                            #     max_amplitude[i] = j
                            #     count = 5
                            # else:
                            #     new_seq[max_amplitude[i]] = "0000ff"
                            #     if count == 0:
                            #         max_amplitude[i] = max_amplitude[i]-6
                            #         count = 5
                            #     else:
                            #         count -= 1
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