
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft
import sys
import time
import math
import os
import sacn
import signal

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

        signal.signal(signal.SIGINT, self.signal_handler)

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

    def signal_handler(self, sig, frame):
        print('Stopping the sender')
        self.sender.stop()
        sys.exit(0)

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
        
        self.sender = sacn.sACNsender()
        self.sender.start()

        for u in range(1,97):
            self.sender.activate_output(u)
            self.sender[u].destination = "192.168.7.2"

        while True:
            data = self.stream.read(self.CHUNK, False)
            data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)

            yf = fft(data_int)
            yfData = np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK)

            bandData = self.createBands(yfData)
            for i in range(21):
                row = []
                height = bandData[i]*300
                for r in range(2):
                    for a in range(int(height)):
                        if(a%3==0):
                            row.append(255)
                            row.append(0)
                            row.append(0)
                    for k in range(int(192-height)):
                        row.append(0)
                self.sender[i+1].dmx_data = row
                # time.sleep(0.003)
            self.clear()
            print(bandData)
            self.line1.set_ydata(bandData)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            

if __name__ == '__main__':
    AudioStream()
