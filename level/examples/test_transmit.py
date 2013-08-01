#!/usr/bin/python

# python ~/workspace/level_basestation/pre-cog/examples/simple_trx.py --port 12345 --radio-addr 85 --dest-addr 86 --args serial=E8R10Z2B1
# python ~/workspace/level_basestation/pre-cog/examples/simple_trx.py --port 12346 --radio-addr 86 --dest-addr 85 --args serial=E4R11Y0B1

from gnuradio import gr
from gnuradio import uhd
from gnuradio import digital
from gnuradio import blks2
from gnuradio.gr import firdes
import gnuradio.gr.gr_threading as _threading
from gnuradio import level
from gnuradio import extras
from math import pi
from gruel import pmt
import urllib2, time, json

class test_transmit(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "CC430 Transmitter")

        self.sent_pkts = 0

        # 5555 5555 2c6e fd00 0071 da0b e2
        self.packet =  chr(0x55)*4                          # preamble
        self.packet += chr(0x2c) + chr(0x6e)                # sync
        self.packet += chr(0xfc)                            # length
        self.packet += chr(0x00) + chr(0x00) + chr(0x00)    # payload
        self.packet += chr(0x71) + chr(0xda) + chr(0x0b) + chr(0xe2) # CRC (currently incorrect)

        # Variables
        self.samp_rate = samp_rate = 125e3
        self.f_center = f_center = 868e6
        self.bandwidth = bandwidth = 200e3
        self.gain = gain = 5

        self.msgq = msgq = gr.msg_queue()

        # Blocks
        self.uhd_sink = uhd.usrp_sink(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_sink.set_samp_rate(samp_rate)
        self.uhd_sink.set_center_freq(f_center, 0)
        self.uhd_sink.set_gain(gain, 0)
        self.uhd_sink.set_bandwidth(bandwidth, 0)

        self.msg_src = gr.message_source(1, msgq)

        self.msk = level.msk_mod_bc(
            samples_per_symbol=2,
            bt=0.3
        )
        
        # Connections
        self.connect(self.msg_src, self.msk, self.uhd_sink)

    def send_pkt(self, payload):
        msg = gr.message_from_string(str(payload))
        self.msgq.insert_tail(msg)

    def get_top_hn(self):
        try:
            f_page = urllib2.urlopen("http://api.ihackernews.com/page").read()
        except urllib2.HTTPError:
            return "HN returned server error: 0"
        fj = json.loads(f_page)
        title = fj['items'][0]['title']
        score = fj['items'][0]['points']
        return str(title) + ":" + str(score)

    def form_packet(self, payload):
        length = len(payload)
        self.packet =  chr(0x55)*4                          # preamble
        self.packet += chr(0xd3) + chr(0x91)                # sync
        self.packet += chr(length)                          # length
        self.packet += str(payload)
        self.packet += chr(0x71) + chr(0xda) + chr(0x0b) + chr(0xe2) # CRC (currently incorrect)

    def main_loop(self):
        while True:
            payload = self.get_top_hn()
            print payload
            self.packet = self.form_packet(payload)
            self.send_pkt(self.packet)
            self.sent_pkts += 1
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print "\n\nSent Packets:", self.sent_pkts, "\n"
                break

if __name__ == '__main__':
    tx = test_transmit()
    r = gr.enable_realtime_scheduling()
    tx.start()
    tx.main_loop()
