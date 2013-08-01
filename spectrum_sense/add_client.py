import os


#This script is used for adding a new client to the network. Once gnuradio sees a new client device request for bandwidth, it passes the data it got from that packet to this script which gives it a clientID, a frequency, and a bandwidth. It then waits for the client to reply with an ACK and a measurement of the interference it experiences. The database is updated and that information is used to improve the network performance overall (with assign_channels.py)


#Takes in these arguments in this order:
#freq - frequency that the client is transmitting it's beacon on, so it can send information back
#bw - bandwidth that the client is requesting. This is encoded in the packet

def add(freq, bw):
    #For now, we're going to grab the open channel that has the most "goodness" that we know of. This is from a FIFO that spectrum_sense is continiously building.
    #FIXME We should eventually change this to be more intelligent.
    assigned_freq = 
    assigned_bw = 100000 #This is in Hz (ie 100 kHz).  
    #FIXME Dynamically allocate bandwidth
    
