
from gnuradio import gr, uhd
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

import sys

class uhd_interface:
    def __init__(self, istx, args, bandwidth, freq=None,
                 gain=None, spec=None, antenna=None):
        
        if(istx):
            self.u = uhd.usrp_sink(device_addr=args, stream_args=uhd.stream_args('fc32'))
        else:
            self.u = uhd.usrp_source(device_addr=args, stream_args=uhd.stream_args('fc32'))

        # Set the subdevice spec
        if(spec):
            self.u.set_subdev_spec(spec, 0)

        # Set the antenna
        if(antenna):
            self.u.set_antenna(antenna, 0)
        
        self._args = args
        self._ant  = antenna
        self._spec = spec
        self._gain = self.set_gain(gain)
        self._freq = self.set_freq(freq)

        self._rate = self.set_sample_rate(bandwidth)

    def set_sample_rate(self, bandwidth):
        self.u.set_samp_rate(bandwidth)
        actual_bw = self.u.get_samp_rate()
        
        return actual_bw

    def get_sample_rate(self):
        return self.u.get_samp_rate()
    
    def set_gain(self, gain=None):
        if gain is None:
            # if no gain was specified, use the mid-point in dB
            g = self.u.get_gain_range()
            gain = float(g.start()+g.stop())/2
            print "\nNo gain specified."
            print "Setting gain to %f (from [%f, %f])" % \
                (gain, g.start(), g.stop())
        
        self.u.set_gain(gain, 0)
        return gain

    def set_freq(self, freq=None):
        if(freq is None):
            sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
            sys.exit(1)
        
        r = self.u.set_center_freq(freq, 0)
        if r:
            return freq
        else:
            frange = self.u.get_freq_range()
            sys.stderr.write(("\nRequested frequency (%f) out or range [%f, %f]\n") % \
                                 (freq, frange.start(), frange.stop()))
            sys.exit(1)

#-------------------------------------------------------------------#
#   TRANSMITTER
#-------------------------------------------------------------------#

class uhd_transmitter(uhd_interface, gr.hier_block2):
    def __init__(self, args, bandwidth, freq=None, gain=None,
                 spec=None, antenna=None, verbose=False):
        gr.hier_block2.__init__(self, "uhd_transmitter",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(0,0,0))

        # Set up the UHD interface as a transmitter
        uhd_interface.__init__(self, True, args, bandwidth,
                               freq, gain, spec, antenna)

        self.connect(self, self.u)

#-------------------------------------------------------------------#
#   RECEIVER
#-------------------------------------------------------------------#

class uhd_receiver(uhd_interface, gr.hier_block2):
    def __init__(self, args, bandwidth, freq=None, gain=None,
                 spec=None, antenna=None, verbose=False):
        gr.hier_block2.__init__(self, "uhd_receiver",
                                gr.io_signature(0,0,0),
                                gr.io_signature(1,1,gr.sizeof_gr_complex))
      
        # Set up the UHD interface as a receiver
        uhd_interface.__init__(self, False, args, bandwidth,
                               freq, gain, spec, antenna)

        self.connect(self.u, self)
