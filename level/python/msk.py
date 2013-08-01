from gnuradio import gr
from gnuradio import digital
from gnuradio import filter
from math import pi
import numpy

class msk_demod_cf(gr.hier_block2):
    def __init__(self):
        """
        Hierarchical block for MSK demodulation.
    
        The input is the complex modulated signal at baseband
        and the output is a stream of floats.
        """
        # Initialize base class
        gr.hier_block2.__init__(self, "msk_demod",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_float))

        self.sps = 2
        self.bt = 0.35
        self.mu = 0.5
        self.gain_mu = 0.175
        self.freq_error = 0.0
        self.omega_relative_limit = 0.005

        self.omega = self.sps * (1 + self.freq_error)
        self.gain_omega = .25 * self.gain_mu * self.gain_mu        # critically damped

        # Demodulate FM
        sensitivity = (pi / 2) / self.sps
        self.fmdemod = gr.quadrature_demod_cf(1.0 / sensitivity)
        self.invert = gr.multiply_const_vff((-1, ))

        # TODO: this is hardcoded, how to figure out this value?
        self.offset = gr.add_const_vff((-1.2, ))

        # the clock recovery block tracks the symbol clock and resamples as needed.
        # the output of the block is a stream of soft symbols (float)
        self.clock_recovery = digital.clock_recovery_mm_ff(self.omega, self.gain_omega,
                                                               self.mu, self.gain_mu,
                                                               self.omega_relative_limit)

        self.slicer = digital.binary_slicer_fb()

        self.connect(self, self.fmdemod, self.invert, self.clock_recovery, self.offset, self)

class msk_mod_bc(gr.hier_block2):
    def __init__(self, bt = 0.3, samples_per_symbol = 2):
        gr.hier_block2.__init__(self, "msk_demod",
                gr.io_signature(1, 1, gr.sizeof_char),
                gr.io_signature(1, 1, gr.sizeof_gr_complex))

        ntaps = 4 * samples_per_symbol              # up to 3 bits in filter at once
        sensitivity = (pi / 2) / samples_per_symbol # phase change per bit = pi / 2

        # Turn it into NRZ data.
        self.unpack = gr.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.nrz = digital.chunks_to_symbols_bf([-1, 1], 1) # note could also invert bits here

        # Form Gaussian filter
        # Generate Gaussian response (Needs to be convolved with window below).
        self.gaussian_taps = gr.firdes.gaussian(1, samples_per_symbol, bt, ntaps)

        self.sqwave = (1,) * samples_per_symbol       # rectangular window
        self.taps = numpy.convolve(numpy.array(self.gaussian_taps),numpy.array(self.sqwave))
        self.gaussian_filter = filter.interp_fir_filter_fff(samples_per_symbol, self.taps)

        # FM modulation
        self.fmmod = gr.frequency_modulator_fc(sensitivity)

        # TODO: this is hardcoded, how to figure out this value?
        self.offset = gr.add_const_vff((-.5, ))

        # CC430 RF core is inverted with respect to USRP for some reason
        self.invert = gr.multiply_const_vff((-1, ))

        # Connect & Initialize base class
        self.connect(self, self.unpack, self.nrz, self.invert, self.offset, self.gaussian_filter, self.fmmod, self)