
from gnuradio import gr
from gnuradio import eng_notation
from gnuradio import digital

import copy
import sys

class receive_path(gr.hier_block2):
    def __init__(self, rx_callback, options):

	gr.hier_block2.__init__(self, "receive_path",
				gr.io_signature(1, 1, gr.sizeof_gr_complex),
				gr.io_signature(0, 0, 0))


        options = copy.copy(options)    # make a copy so we can destructively modify

        self._verbose     = options.verbose
        self._log         = options.log
        self._rx_callback = rx_callback      # this callback is fired when there's a packet available

        # receiver
        self.ofdm_rx = digital.ofdm_demod(options,
                                          callback=self._rx_callback)

        self.connect(self, self.ofdm_rx)
        self.connect(self.ofdm_rx, self.probe)

        # Display some information about the setup
        if self._verbose:
            self._print_verbage()
        
    def carrier_sensed(self):
        """
        Return True if we think carrier is present.
        """
        #return self.probe.level() > X
        return self.probe.unmuted()
