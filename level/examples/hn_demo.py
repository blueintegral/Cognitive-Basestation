#! /usr/bin/python

# simple demo that transmits the top hacker news post over our network

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
import urllib2, time, json, operator, binascii, sys
import crcmod

crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=False)

class test_transmit(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "CC430 Transmitter")

        self.sent_pkts = 0

        # 5555 5555 2c6e fd00 0071 da0b e2
        self.test_packet =  chr(0x55)*4                          # preamble
        self.test_packet += chr(0x2c) + chr(0x6e)                # sync
        self.test_packet += chr(0xfc)                            # length
        self.test_packet += chr(0x00) + chr(0x00) + chr(0x00)    # payload
        self.test_packet += chr(0xc3) + chr(0xdb)				 # CRC16 (currently incorrect?)

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
            sys.exit("HN returned server error: 0")
        fj = json.loads(f_page)
        title = fj['items'][0]['title'][:50]
        score = fj['items'][0]['points']
        return str(title) + " : " + str(score)

    def form_packet(self, payload):
        length = len(payload)
        crc = crc16_func(chr(length) + payload)
        
        packet =  chr(0x00)							   # guard
        packet += chr(0xAA)*4                          # preamble
        packet += chr(0xD3) + chr(0x91)                # sync
        packet += chr(length)                          # length
        packet += payload
        packet += chr(crc >> 8) + chr(crc & 0xFF)      # crc, sorry for bit hackery
        packet += chr(0xFF) + chr(0x00)							   # guard
        return packet

    def main_loop(self, max_pkts):
        payload = self.get_top_hn()
        while self.sent_pkts < max_pkts:
            if not self.sent_pkts % 100:
                payload = self.get_top_hn()
            packet = self.form_packet(payload)
            self.send_pkt(packet)
            self.sent_pkts += 1
            try:
                print payload
                time.sleep(1)
                pass
            except KeyboardInterrupt:
                print "\n\nSent Packets:", self.sent_pkts, "\n"
                break

if __name__ == '__main__':
    tx = test_transmit()
    r = gr.enable_realtime_scheduling()
    tx.start()
    tx.main_loop(2000)
