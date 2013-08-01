#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Cw
# Generated: Fri Nov  2 15:30:03 2012
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import gnuradio.extras as gr_extras
import wx

class cw(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Cw")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 500e3

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		self.uhd_usrp_sink_0.set_center_freq(520e6, 0)
		self.uhd_usrp_sink_0.set_gain(25, 0)
		self.uhd_usrp_sink_0.set_bandwidth(50e3, 0)
		self.extras_signal_source_0 = gr_extras.signal_source_fc32()
		self.extras_signal_source_0.set_waveform("COSINE")
		self.extras_signal_source_0.set_offset(0)
		self.extras_signal_source_0.set_amplitude(1.0)
		self.extras_signal_source_0.set_frequency(samp_rate, 1000)

		##################################################
		# Connections
		##################################################
		self.connect((self.extras_signal_source_0, 0), (self.uhd_usrp_sink_0, 0))

# QT sink close method reimplementation

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.extras_signal_source_0.set_frequency(self.samp_rate, 1000)
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = cw()
	tb.Run(True)

