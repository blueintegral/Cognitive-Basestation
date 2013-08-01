
from gnuradio import gr
from gnuradio import eng_notation
from gnuradio import digital

import copy
import sys

class transmit_path(gr.hier_block2): 
    def __init__(self):

    	gr.hier_block2.__init__(self, "transmit_path",
    				gr.io_signature(0, 0, 0),
    				gr.io_signature(1, 1, gr.sizeof_gr_complex))

        self.msgq = msgq = gr.msg_queue()
        self.msg_src = gr.message_source(1, msgq)

        self.msk = digital.gmsk_mod(
            samples_per_symbol=2,
            bt=0.3
        )

        # Connections
        self.connect(self.msg_src, self.msk, self)

    def send_pkt(self, payload='', eof=False):
        print self.msgq.count()
        if eof:
            msg = gr.message(1) # tell self._pkt_input we're not sending any more packets
        else:
            msg = gr.message_from_string(payload)
        self.msgq.insert_tail(msg)
