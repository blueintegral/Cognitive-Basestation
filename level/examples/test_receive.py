#!/usr/bin/python

from gnuradio import gr
from gnuradio import uhd
from gnuradio import digital
from gnuradio import blks2
from gnuradio.gr import firdes
from gnuradio import level
from math import pi

class msk_rx(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "CC1101 Burst Detector")

        def rx_callback():
            print "Callback Fired"

        # Variables
        self.samp_rate = samp_rate = 125e3
        self.f_center = f_center = 868e6
        self.bandwidth = bandwidth = 200e3
        self.gain = gain = 5

        # Blocks
        self.uhd_src = uhd.usrp_source(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_src.set_subdev_spec("A:0", 0)
        self.uhd_src.set_samp_rate(samp_rate)
        self.uhd_src.set_center_freq(f_center, 0)
        self.uhd_src.set_gain(gain, 0)
        self.uhd_src.set_antenna("TX/RX", 0)
        self.uhd_src.set_bandwidth(bandwidth, 0)

        self.uhd_src.set_samp_rate(self.samp_rate)
        self.uhd_src.set_center_freq(self.f_center, 0)
        self.uhd_src.set_gain(self.gain, 0)

        self.packet_receiver = level.cc1k_demod_pkts(callback=rx_callback())

        # Connections
        self.connect(self.uhd_src, self.packet_receiver)

if __name__ == '__main__':
    rx = msk_rx()
    r = gr.enable_realtime_scheduling()
    rx.start()
    raw_input('Press Enter to quit: ')
    rx.stop()
