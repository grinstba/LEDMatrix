import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft
import sys
import time
import math
import os


class AudioStream(object):
    def __init__(self):

        # stream constants
        self.CHUNK = 2048 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False
        self.bins = [3,3,3,4,10,14,17,26,34,59,79,139,159,159,229,249,299,499,599,599,794]
        self.numBands = len(self.bins)
        self.fig = None
        self.line1 = None

        self.clear = lambda: os.system('clear')

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
        self.startSpectrum()

    def createBands(self, data):
        bandData = [0] * self.numBands
        index = 25
        for k in range(self.numBands):
            max = 0
            for _ in range(self.bins[k]):
                if(data[index] > max):
                   max = data[index]
                index+= 1

            bandData[k] = max

        return bandData

    def setupPlot(self):
        x = np.linspace(0,self.numBands - 1,self.numBands)
        y = [0] * self.numBands
        plt.ion()
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        ax.set_ylim(0, 2)
        self.line1, = ax.plot(x, y, 'b-')
            
    def startSpectrum(self):

        self.setupPlot()

        while True:
            data = self.stream.read(self.CHUNK, False)
            data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)

            yf = fft(data_int)
            yfData = np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK)

            bandData = self.createBands(yfData)
            self.clear()
            print(bandData)
            self.line1.set_ydata(bandData)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            

if __name__ == '__main__':
    AudioStream()
