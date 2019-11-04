#!/usr/bin/env python3
import Adafruit_BBIO.ADC as ADC
import time
import numpy as np

ADC.setup()
x=0
while(x<10):
	current = []
	for i in range(0,1024,1):
		value = ADC.read("AIN0")
		current.append(value)
	print(current)
	time.sleep(0.05)	
	x = x + 1
	processed = np.fft.fft(current)
	print(processed)


