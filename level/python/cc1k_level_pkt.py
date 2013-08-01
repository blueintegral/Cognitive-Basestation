from math import pi
from gnuradio import gr
from gnuradio import digital
from level_swig import *
from msk import msk_demod_cf
import gnuradio.gr.gr_threading as _threading
import struct

class cc1k_demod_pkts(gr.hier_block2):
    """
    cc1101 demodulator that is a GNU Radio sink.

    The input is complex baseband.  When packets are demodulated, they are passed to the
    app via the callback.
    """

    def __init__(self, preamble=None, callback=None):
        """
    	Hierarchical block for binary FSK demodulation.

    	The input is the complex modulated signal at baseband.
            Demodulated packets are sent to the handler.

            @param preamble: 32-bit preamble
            @type preamble: string
            @param callback:  function of two args: ok, payload
            @type callback: ok: bool; payload: string

            See cc1101_demod for remaining parameters.
    	"""

        gr.hier_block2.__init__(self, "demod_pkts",
            gr.io_signature(1, 1, gr.sizeof_gr_complex), # Input signature
            gr.io_signature(0, 0, 0))                    # Output signature

        if preamble is None:
            preamble = chr(0b01010101) + chr(0b01010101) + chr(0b01010101) + chr(0b01010101)
        self._preamble = preamble

        self._rcvd_pktq = gr.msg_queue()          # holds packets from the PHY
        self.msk_demod = msk_demod_cf()
        self._packet_sink = packet_sink(map(ord, preamble), self._rcvd_pktq)
        
        self.connect(self, self.msk_demod, self._packet_sink)
      
        self._watcher = _queue_watcher_thread(self._rcvd_pktq, callback)

    def carrier_sensed(self):
        return self._packet_sink.carrier_sensed()


class _queue_watcher_thread(_threading.Thread):
    def __init__(self, rcvd_pktq, callback):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.rcvd_pktq = rcvd_pktq
        self.callback = callback
        self.keep_running = True
        self.start()

    def stop(self):
        self.keep_running = False
        
    def run(self):
        while self.keep_running:
            print "cc1k_level_pkt: waiting for packet"
            msg = self.rcvd_pktq.delete_head()
            payload = msg.to_string()
            print "received packet "
            print payload.encode("hex")
            print payload.encode("ascii")
