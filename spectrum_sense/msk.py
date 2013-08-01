from gnuradio import gr
from gnuradio import digital
from math import pi

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
        self.offset = gr.add_const_vff((-1.4, ))

        # the clock recovery block tracks the symbol clock and resamples as needed.
        # the output of the block is a stream of soft symbols (float)
        self.clock_recovery = digital.clock_recovery_mm_ff(self.omega, self.gain_omega,
                                                               self.mu, self.gain_mu,
                                                               self.omega_relative_limit)

        self.slicer = digital.binary_slicer_fb()

        self.connect(self, self.fmdemod, self.invert, self.clock_recovery, self.offset, self)