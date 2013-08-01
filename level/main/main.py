#! /usr/bin/python

import binascii, time
from struct import *
from gnuradio import gr, uhd
from gnuradio import level

# from current dir
from receive_path import receive_path
from transmit_path import transmit_path
from uhd_interface import uhd_transmitter
from uhd_interface import uhd_receiver

# /////////////////////////////////////////////////////////////////////////////
#                                globals
# /////////////////////////////////////////////////////////////////////////////

# Variables
samp_rate = 125e3
f_center = 868e6
bandwidth = 200e3
gain = 5

# /////////////////////////////////////////////////////////////////////////////
#                               flow graph
# /////////////////////////////////////////////////////////////////////////////

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.uhd_sink = uhd.usrp_sink(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_sink.set_samp_rate(samp_rate)
        self.uhd_sink.set_center_freq(f_center, 0)
        self.uhd_sink.set_gain(gain, 0)
        self.uhd_sink.set_bandwidth(bandwidth, 0)

        self.txpath = transmit_path()
        #self.rxpath = receive_path(callback, options)

        self.connect(self.txpath, self.uhd_sink)
        #self.connect(self.source, self.rxpath)

    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()

    def set_freq(self, target_freq):
        """
        Set the center frequency we're interested in.
        """
        self.u_snk.set_freq(target_freq)
        self.u_src.set_freq(target_freq)

class proto_mac(object):

    def __init__(self):
        self.tb = None             # top block (access to PHY)

    def set_flow_graph(self, tb):
        self.tb = tb

    def main_loop(self):
        """
        Main loop for MAC.
        Only returns if we get an error reading from TUN.
        """
        while True:
            payload = "test"
            time.sleep(1)
            if not payload:
                self.tb.txpath.send_pkt(eof=True)
                break
            else:
                self.tb.txpath.send_pkt(payload)

#def packetize(payload):
#	preamble = bin(0x5555)[2:]
#	sync = bin(0x2C6E)[2:]
#	length = bin(len(payload))[2:]
#	fcs = bin(binascii.crc32(payload))
#	b_payload = bin(int(binascii.hexlify('hello'), 16))[2:]
#	packet = preamble + sync + length + b_payload
#	print fcs
#	out = open('packet.bin', 'w')
#	out.write(packet)

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    r = gr.enable_realtime_scheduling()

    # build the graph (PHY)
    tb = my_top_block()
    mac = proto_mac()

    mac.set_flow_graph(tb)    # give the MAC a handle for the PHY
    tb.start()    			  # Start executing the flow graph (runs in separate threads)

    mac.main_loop()    		  # don't expect this to return...

    tb.stop()     			  # but if it does, tell flow graph to stop.
    tb.wait()     			  # wait for it to finish
