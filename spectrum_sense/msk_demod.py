from gnuradio import digital
from gnuradio import blks2
from gnuradio import gr
from gnuradio import uhd
from gnuradio.gr import firdes
import msk
import math 
import time, re

#This script is different rom msk_demod_dev in a couple ways. It's set up to be called as a function, not run as a script. It's also designed to take in data already gotten from the USRP rather than get it itself.

def msk_demod(samp_rate, f_center, bandwidth): 
	gain = 5
	decimation = 2
	gr.enable_realtime_scheduling()
	
