
#!/usr/bin/env python3
import sacn
import time
import numpy

sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].destination = "fpp"  # or provide unicast information
row=[]
#for i in range(0,192):
#	if(i%3==0):
#		row.append(255)
#		row.append(0)
#		row.append(0)
#for i in range(0,192):
#        if(i%3==0):
#                row.append(0)
#                row.append(255)
#                row.append(0)#

sender[1].dmx_data = (255,0)  # some test DMX data
time.sleep(.05)
sender.stop()  # do not forget to stop the sender

