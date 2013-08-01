from gnuradio import gr
from gnuradio import digital
from math import pi

class fsk_demod_cf(gr.hier_block2):
    def __init__(self):
        """
        Hierarchical block for FSK demodulation.
    
        The input is the complex modulated signal at baseband
        and the output is a stream of floats.
        """
        # Initialize base class
        gr.hier_block2.__init__(self, "fsk_demod",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_float))

        # Variables
        self.sps = sps = 2
        self.sensitivity = sensitivity = (pi / 2) / sps
        self.alpha = alpha = 0.0512/sps

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

        # Connections
        self.connect(self.fm_demod, (self.add, 0))
        self.connect(self.fm_demod, self.freq_offset, (self.add, 1))
        self.connect(self, self.fm_demod)
        self.connect(self.add, self.clock_recovery, self.invert, self)