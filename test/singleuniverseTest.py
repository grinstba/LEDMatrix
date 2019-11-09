#!/usr/bin/env python3
import sacn
import time
import numpy

sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
sender.start()  # start the sending thread
#sender.activate_output(1)
#sender[1].destination = "192.168.7.2"
row = []
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].destination = "192.168.7.2"  # or provide unicast information
for i in range(0,194):
	if(i%3==0):
		row.append(255)
		row.append(0)
		row.append(0)
sender[1].dmx_data = row
time.sleep(.003)
sender.stop()  # do not forget to stop the sender
