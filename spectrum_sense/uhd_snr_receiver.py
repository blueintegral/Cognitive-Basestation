#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Uhd Snr Receiver
# Generated: Fri Oct  5 10:13:32 2012
##################################################

from PyQt4 import Qt
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import sip
import sys

class uhd_snr_receiver(gr.top_block, Qt.QWidget):

	def __init__(self):
		gr.top_block.__init__(self, "Uhd Snr Receiver")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Uhd Snr Receiver")
		self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
		self.top_scroll_layout = Qt.QVBoxLayout()
		self.setLayout(self.top_scroll_layout)
		self.top_scroll = Qt.QScrollArea()
		self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
		self.top_scroll_layout.addWidget(self.top_scroll)
		self.top_scroll.setWidgetResizable(True)
		self.top_widget = Qt.QWidget()
		self.top_scroll.setWidget(self.top_widget)
		self.top_layout = Qt.QVBoxLayout(self.top_widget)
		self.top_grid_layout = Qt.QGridLayout()
		self.top_layout.addLayout(self.top_grid_layout)

		self.settings = Qt.QSettings("GNU Radio", "uhd_snr_receiver")
		self.restoreGeometry(self.settings.value("geometry").toByteArray())


		##################################################
		# Variables
		##################################################
		self.sps = sps = 4
		self.nfilts = nfilts = 32
		self.samp_rate = samp_rate = 1e6
		self.rrc_taps = rrc_taps = filter.firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 11*sps*nfilts)
		self.gain = gain = 15
		self.freq = freq = 431e6
		self.fine_freq = fine_freq = -28400

		##################################################
		# Blocks
		##################################################
		self._gain_layout = Qt.QVBoxLayout()
		self._gain_tool_bar = Qt.QToolBar(self)
		self._gain_layout.addWidget(self._gain_tool_bar)
		self._gain_tool_bar.addWidget(Qt.QLabel("RX Gain"+": "))
		self._gain_counter = Qwt.QwtCounter()
		self._gain_counter.setRange(0, 31.5, 0.5)
		self._gain_counter.setNumButtons(2)
		self._gain_counter.setValue(self.gain)
		self._gain_tool_bar.addWidget(self._gain_counter)
		self._gain_counter.valueChanged.connect(self.set_gain)
		self._gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
		self._gain_slider.setRange(0, 31.5, 0.5)
		self._gain_slider.setValue(self.gain)
		self._gain_slider.setMinimumWidth(200)
		self._gain_slider.valueChanged.connect(self.set_gain)
		self._gain_layout.addWidget(self._gain_slider)
		self.top_layout.addLayout(self._gain_layout)
		self._freq_layout = Qt.QVBoxLayout()
		self._freq_tool_bar = Qt.QToolBar(self)
		self._freq_layout.addWidget(self._freq_tool_bar)
		self._freq_tool_bar.addWidget(Qt.QLabel("Frequency"+": "))
		self._freq_counter = Qwt.QwtCounter()
		self._freq_counter.setRange(400e6, 500e6, 1e6)
		self._freq_counter.setNumButtons(2)
		self._freq_counter.setValue(self.freq)
		self._freq_tool_bar.addWidget(self._freq_counter)
		self._freq_counter.valueChanged.connect(self.set_freq)
		self._freq_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
		self._freq_slider.setRange(400e6, 500e6, 1e6)
		self._freq_slider.setValue(self.freq)
		self._freq_slider.setMinimumWidth(200)
		self._freq_slider.valueChanged.connect(self.set_freq)
		self._freq_layout.addWidget(self._freq_slider)
		self.top_grid_layout.addLayout(self._freq_layout, 2,0,1,1)
		self._fine_freq_layout = Qt.QVBoxLayout()
		self._fine_freq_tool_bar = Qt.QToolBar(self)
		self._fine_freq_layout.addWidget(self._fine_freq_tool_bar)
		self._fine_freq_tool_bar.addWidget(Qt.QLabel("Fine Frequency"+": "))
		self._fine_freq_counter = Qwt.QwtCounter()
		self._fine_freq_counter.setRange(-50e3, 50e3, 100)
		self._fine_freq_counter.setNumButtons(2)
		self._fine_freq_counter.setValue(self.fine_freq)
		self._fine_freq_tool_bar.addWidget(self._fine_freq_counter)
		self._fine_freq_counter.valueChanged.connect(self.set_fine_freq)
		self._fine_freq_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
		self._fine_freq_slider.setRange(-50e3, 50e3, 100)
		self._fine_freq_slider.setValue(self.fine_freq)
		self._fine_freq_slider.setMinimumWidth(200)
		self._fine_freq_slider.valueChanged.connect(self.set_fine_freq)
		self._fine_freq_layout.addWidget(self._fine_freq_slider)
		self.top_grid_layout.addLayout(self._fine_freq_layout, 2,1,1,1)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(freq + fine_freq, 0)
		self.uhd_usrp_source_0.set_gain(gain, 0)
		self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
		self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
			500, #size
			samp_rate, #bw
			"QT GUI Plot", #name
			3 #number of inputs
		)
		self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
		self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 0,0,1,1)
		self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
			1024, #size
			firdes.WIN_BLACKMAN_hARRIS, #wintype
			0, #fc
			samp_rate, #bw
			"QT GUI Plot", #name
			1 #number of inputs
		)
		self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1,0,1,2)
		self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
			1024, #size
			"QT GUI Plot", #name
			2 #number of inputs
		)
		self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 0,1,1,1)
		self.gr_null_sink_0_1 = gr.null_sink(gr.sizeof_gr_complex*1)
		self.gr_null_sink_0_0 = gr.null_sink(gr.sizeof_gr_complex*1)
		self.gr_null_sink_0 = gr.null_sink(gr.sizeof_gr_complex*1)
		self.gr_multiply_xx_0 = gr.multiply_vcc(1)
		self.gr_agc2_xx_0 = gr.agc2_cc(1e-1, 1e-2, 1.0, 1.0, 0.0)
		self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 2*3.14/100.0, (rrc_taps), nfilts, nfilts/2, 1.5, 1)
		self.digital_mpsk_snr_est_cc_0_1 = digital.mpsk_snr_est_cc(3, 10000, 0.001)
		self.digital_mpsk_snr_est_cc_0_0 = digital.mpsk_snr_est_cc(2, 10000, 0.001)
		self.digital_mpsk_snr_est_cc_0 = digital.mpsk_snr_est_cc(0, 10000, 0.001)
		self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(15, 0.010, 1, digital.constellation_qpsk().base())
		self.digital_costas_loop_cc_0 = digital.costas_loop_cc(2*3.14/100.0, 4)

		##################################################
		# Connections
		##################################################
		self.connect((self.digital_mpsk_snr_est_cc_0, 0), (self.gr_null_sink_0, 0))
		self.connect((self.digital_mpsk_snr_est_cc_0, 1), (self.qtgui_time_sink_x_0_0, 0))
		self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_mpsk_snr_est_cc_0, 0))
		self.connect((self.gr_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
		self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.qtgui_const_sink_x_0, 1))
		self.connect((self.gr_agc2_xx_0, 0), (self.gr_multiply_xx_0, 3))
		self.connect((self.gr_agc2_xx_0, 0), (self.gr_multiply_xx_0, 2))
		self.connect((self.gr_agc2_xx_0, 0), (self.gr_multiply_xx_0, 1))
		self.connect((self.gr_agc2_xx_0, 0), (self.gr_multiply_xx_0, 0))
		self.connect((self.gr_agc2_xx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
		self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))
		self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
		self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.gr_agc2_xx_0, 0))
		self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_mpsk_snr_est_cc_0_0, 0))
		self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_mpsk_snr_est_cc_0_1, 0))
		self.connect((self.digital_mpsk_snr_est_cc_0_1, 0), (self.gr_null_sink_0_1, 0))
		self.connect((self.digital_mpsk_snr_est_cc_0_0, 0), (self.gr_null_sink_0_0, 0))
		self.connect((self.digital_mpsk_snr_est_cc_0_0, 1), (self.qtgui_time_sink_x_0_0, 1))
		self.connect((self.digital_mpsk_snr_est_cc_0_1, 1), (self.qtgui_time_sink_x_0_0, 2))

# QT sink close method reimplementation
	def closeEvent(self, event):
		self.settings = Qt.QSettings("GNU Radio", "uhd_snr_receiver")
		self.settings.setValue("geometry", self.saveGeometry())
		event.accept()

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		self.set_rrc_taps(filter.firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

	def get_nfilts(self):
		return self.nfilts

	def set_nfilts(self, nfilts):
		self.nfilts = nfilts
		self.set_rrc_taps(filter.firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

	def get_rrc_taps(self):
		return self.rrc_taps

	def set_rrc_taps(self, rrc_taps):
		self.rrc_taps = rrc_taps
		self.digital_pfb_clock_sync_xxx_0.set_taps((self.rrc_taps))

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self._gain_counter.setValue(self.gain)
		self._gain_slider.setValue(self.gain)
		self.uhd_usrp_source_0.set_gain(self.gain, 0)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self._freq_counter.setValue(self.freq)
		self._freq_slider.setValue(self.freq)
		self.uhd_usrp_source_0.set_center_freq(self.freq + self.fine_freq, 0)

	def get_fine_freq(self):
		return self.fine_freq

	def set_fine_freq(self, fine_freq):
		self.fine_freq = fine_freq
		self._fine_freq_counter.setValue(self.fine_freq)
		self._fine_freq_slider.setValue(self.fine_freq)
		self.uhd_usrp_source_0.set_center_freq(self.freq + self.fine_freq, 0)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	qapp = Qt.QApplication(sys.argv)
	tb = uhd_snr_receiver()
	tb.start()
	tb.show()
	qapp.exec_()
	tb.stop()
	tb = None #to clean up Qt widgets

