#!/usr/bin/env python3
import Adafruit_BBIO.ADC as ADC
import time
import numpy as np
import matplotlib.pyplot as plt

ADC.setup()
x=0
Fs = 44100
T = 1/Fs
samples = 1024
while(x<1):
	current = []
	for i in range(0,samples,1):
		value = ADC.read("AIN0")
		current.append(value)
		time.sleep(T)
	print(current)	
	x = x + 1
	processed = np.fft.fft(current)
	print(processed)
xData = np.linspace(0,Fs/2,samples/2)
plt.figure(num=1, figsize=(8,6))
plt.plot(xData, 2/samples * np.abs(processed[:samples//2]))
plt.xscale('log')
plt.savefig('spectrogram.png', format='png')
