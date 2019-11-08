
#!/usr/bin/env python3
import sacn
import time
import numpy

sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
sender.start()  # start the sending thread
#sender.activate_output(1)
#sender[1].destination = "192.168.7.2"
row = []
rows = [row]*96
for u in range(1,97):
	sender.activate_output(u)  # start sending out data in the 1st universe
	sender[u].destination = "192.168.7.2"  # or provide unicast information
	#row=[]
	for i in range(0,383):
		if(i%3==0):
			row.append(0)
			row.append(0)
			row.append(0)
#sender[1].dmx_data = row
	rows[u-1] = row
	sender[u].dmx_data = rows[u-1]  # some test DMX data
	time.sleep(.003)
sender.stop()  # do not forget to stop the sender

