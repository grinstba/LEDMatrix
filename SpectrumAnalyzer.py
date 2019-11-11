import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft
import sys
import time
import math
import sacn
import signal
import keyboard

class AudioStream(object):
    def __init__(self):

        # stream constants
        self.CHUNK = 2048 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.bins = [3,3,3,4,6,6,8,8,10,10,14,15,15,15,20,20,20,25,25,30,50]
        self.numBands = len(self.bins)
        self.fig = None
        self.line1 = None
        self.modes = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.mode = 2
        self.numColors = 9

        signal.signal(signal.SIGINT, self.signal_handler)
        
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
    
    def addRed(self, row):
        row.append(255)
        row.append(0)
        row.append(0)
    
    def addBlue(self, row):
        row.append(0)
        row.append(255)
        row.append(0)

    def addGreen(self, row):
        row.append(0)
        row.append(0)
        row.append(255)
    
    def addTeal(self, row):
        row.append(0)
        row.append(255)
        row.append(255)

    def addSeafoam(self, row):
        row.append(51)
        row.append(255)
        row.append(153)

    def addOrange(self, row):
        row.append(255)
        row.append(153)
        row.append(51)

    def addPurple(self, row):
        row.append(153)
        row.append(51)
        row.append(255)

    def addPink(self, row):
        row.append(253)
        row.append(51)
        row.append(255)

    def addYellow(self, row):
        row.append(255)
        row.append(255)
        row.append(0)

    def createBands(self, data):
        bandData = [0] * self.numBands
        index = 6
        for k in range(self.numBands):
            max = 0
            for _ in range(self.bins[k]):
                if(data[index] > max):
                   max = data[index]
                index+= 1

            bandData[k] = max

        return bandData

    def switchMode(self):
        self.mode = (self.mode + 1) % len(self.modes)

    def getColor(self):
        return self.modes[self.mode]
            
    def startSpectrum(self):
        
        self.sender = sacn.sACNsender()
        self.sender.start()

        for u in range(1,97):
            self.sender.activate_output(u)
            self.sender[u].destination = "192.168.7.2"

        keyboard.add_hotkey('enter', lambda: self.switchMode())
        
        while True:
            data = self.stream.read(self.CHUNK, False)
            data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)

            yf = fft(data_int)
            yfData = np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK)

            bandData = self.createBands(yfData)
            self.modes[0] = (self.modes[0] + 1) % self.numColors

            for i in range(21):
                self.modes[1] = (self.modes[1] + 1) % self.numColors
                row = []
                height = int(bandData[i]*300)
                zeros = 64 - height 
                
                for r in range(2):
                    for a in range(height):
                        colorInt = self.getColor()
                        if(colorInt==0):
                            self.addRed(row)
                        elif(colorInt==1):
                            self.addBlue(row)
                        elif(colorInt==2):
                            self.addGreen(row)
                        elif(colorInt==3):
                            self.addTeal(row)
                        elif(colorInt==4):
                            self.addSeafoam(row)
                        elif(colorInt==5):
                            self.addOrange(row)
                        elif(colorInt==6):
                            self.addPurple(row)
                        elif(colorInt==7):
                            self.addPink(row)
                        elif(colorInt==8):
                            self.addYellow(row)
                    for k in range(zeros):
                            row.append(0)
                            row.append(0)
                            row.append(0)
                for b in range(3):
                    self.sender[i*4+(b+1)+7].dmx_data = row
                    # time.sleep(0.0001)

if __name__ == '__main__':
    AudioStream()
