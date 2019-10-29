#!/usr/bin/env python3
import sacn
import time

sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
sender.start()  # start the sending thread

for univ in range(1, 72):
    sender.activate_output(univ)  # start sending out data in the 1st universe
    # sender[univ].multicast = False  # set multicast to True
    sender[univ].destination = "fpp"  # or provide unicast information.
print("Universes set")
for univ in range(1, 72):
    # Keep in mind that if multicast is on, unicast is not used
    sender[univ].dmx_data = (0, 255, 0, 255, 0, 0, 255, 255, 255)  # some test DMX data
    #row = []
    #for i in range(0, 510, 3):
       # if ((i % 15) == 0):
       #     row.append(255)
       #     row.append(0)
       #     row.append(0)
            
    #sender[univ].dmx_data = row
    time.sleep(0.1)
sender.stop()  # do not forget to stop the sender
