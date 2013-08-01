#!/usr/bin/env python

from gnuradio import digital
from gnuradio import gr
from gnuradio import uhd
from gnuradio.gr import firdes
from math import pi
import time

class simple_fsk_demod(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "FSK Demod Demo")

		# Variables
		self.symbol_rate = symbol_rate = 125e3
		self.samp_rate = samp_rate = symbol_rate
		self.f_center = f_center = 868e6
		self.sps = sps = 2
		self.sensitivity = sensitivity = (pi / 2) / sps
		self.alpha = alpha = 0.0512/sps
		self.bandwidth = bandwidth = 100e3

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
		self.uhd_usrp_source_0.set_gain(0, 0)
		self.uhd_usrp_source_0.set_bandwidth(bandwidth, 0)

		self.fm_demod = gr.quadrature_demod_cf(1 / sensitivity)
		
		self.freq_offset = gr.single_pole_iir_filter_ff(alpha)
		self.sub = gr.sub_ff()
		self.add = gr.add_ff()
		self.multiply = gr.multiply_ff()
		self.invert = gr.multiply_const_vff((-1, ))

		# recover the clock
		omega = sps
		gain_mu = 0.03
		mu = 0.5
		omega_relative_limit = 0.0002
		freq_error = 0.0
		gain_omega = .25 * gain_mu * gain_mu        # critically damped
		self.clock_recovery = digital.clock_recovery_mm_ff(omega, gain_omega, mu, gain_mu, omega_relative_limit)

		self.slice = digital.binary_slicer_fb()
		self.sink = gr.vector_sink_b(1)
		self.file_sink = gr.file_sink(gr.sizeof_char, 'fsk_dump.log')

		# Connections
		self.connect(self.fm_demod, (self.add, 0))
		self.connect(self.fm_demod, self.freq_offset, (self.add, 1))
		self.connect(self.uhd_usrp_source_0, self.fm_demod)
		self.connect(self.add, self.clock_recovery, self.invert, self.slice, self.file_sink)
		self.connect(self.slice, self.sink)

if __name__ == '__main__':
	gr.enable_realtime_scheduling()
	tb = simple_fsk_demod()
	tb.start()
	time.sleep(.1)
	tb.stop()
	#sink_data = tb.sink.data()
	#ones = len([x for x in sink_data if x is 1])
	#print float(ones) / len(sink_data)
	#print sink_data[-1000:]

