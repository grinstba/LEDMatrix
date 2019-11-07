"""
    Notebook for streaming data from a microphone in realtime

    audio is captured using pyaudio
    then converted from binary data to ints using struct
    then displayed using matplotlib

    scipy.fftpack computes the FFT

    if you don't have pyaudio, then run

    >>> pip install pyaudio

    note: with 2048 samples per chunk, I'm getting 20FPS
    when also running the spectrum, its about 15FPS
"""
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
# from pyqtgraph.Qt import QtGui, QtCore
# import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time


class AudioStream(object):
    def __init__(self):

        # stream constants
        self.CHUNK = 2048 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False

        # stream object
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        self.fft()

    def fft(self):
        while True:
            data = self.stream.read(self.CHUNK, False)
            data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)
            data_np = np.array(data_int, dtype='b')[::2] + 128

            yf = fft(data_int, 64)
            yff = np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK)
            print(yff)


if __name__ == '__main__':
    AudioStream()
