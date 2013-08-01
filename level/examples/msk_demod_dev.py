#!/usr/bin/env python

from gnuradio import digital
from gnuradio import blks2
from gnuradio import gr
from gnuradio import uhd
from gnuradio.gr import firdes
from gnuradio.level import msk
from math import pi
import time, re

class msk_demod_dev(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "MSK Demod Demo")

		# Variables
		self.samp_rate = samp_rate = 125e3
		self.f_center = f_center = 868e6
		self.bandwidth = bandwidth = 500e3
		self.gain = gain = 5
		self.decimation = decimation = 2

		# Blocks
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(f_center, 0)
		self.uhd_usrp_source_0.set_gain(gain, 0)
		self.uhd_usrp_source_0.set_bandwidth(bandwidth, 0)

		self.msk_demod = msk.msk_demod_cf()

		self.slicer = digital.binary_slicer_fb()
		self.slicer2 = digital.binary_slicer_fb()

		self.offset = gr.add_const_vff((0, ))

		self.sink = gr.vector_sink_b(1)
		self.f_sink = gr.vector_sink_f(1)
		self.file_sink = gr.file_sink(gr.sizeof_char, 'fsk_dump.log')

		# Connections
		self.connect(self.uhd_usrp_source_0, self.msk_demod, self.offset, self.slicer, self.sink)
		self.connect(self.offset, self.f_sink)
		self.connect(self.offset, self.slicer2, self.file_sink)

def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

if __name__ == '__main__':
	gr.enable_realtime_scheduling()
	tb = msk_demod_dev()
	tb.start()
	time.sleep(1)
	tb.stop()
	sink_data = list(tb.sink.data())
	f_sink_data = list(tb.f_sink.data())
	sink_str = ''.join(map(str,sink_data))
	ones = len([x for x in sink_data if x is 1])
	preamble = '10'*4*4
	sync = '1101001110010001'
	payload = '1111'*15
	print float(ones) / len(sink_data)
	print len(sink_data)
	packet_indices = [l.start() for l in re.finditer(payload, sink_str[2500:])]
	print packet_indices
	for packet in packet_indices:
		packet = packet + 2500
		print sink_str[packet-50:packet+200]
		print ''
		print f_sink_data[packet-50:packet+200]
		print ''
	preambles = [m.start() for m in re.finditer(preamble, sink_str)]
	print "preamble:", preambles