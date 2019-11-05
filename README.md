# ECE434 Project - LED Matrix  

### install.sh  
Run this file to install all the needed packages to run this project.  
> sacn - this library is used to open a communication link between the Bone and the e1.31 protocol  
> e131 - this library is used to control the individual LEDs on the LED matrices via universes setup in falcon player  
> numpy-python3 - this library is used to perform Fast Fourier Transforms, or FFT, on the incoming audio signal  

### test/universeTest.py  
This file is used to test the configuration of the LED matrices and their respected universes setup via falcon player. 
Universes are setup to control one or two full columns so that it is easer to light up our LED spectrometer.  

### test/audioInputTest.py  
This file is used to test our analog pins to see if/how they are reading in audio data. This file also performs FFT 
analysis on the audio input and creates a plot of the frequency spectrum so that we can test the accuracy of the calculated
frequency domain.  