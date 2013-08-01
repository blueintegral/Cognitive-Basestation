#! /usr/bin/python

import os, struct, time, mmap
from fcntl import ioctl

# Linux specific...
# TUNSETIFF ifr flags from <linux/tun_if.h>

IFF_TUN		= 0x0001   # tunnel IP packets
IFF_TAP		= 0x0002   # tunnel ethernet frames
IFF_NO_PI	= 0x1000   # don't pass extra packet info
IFF_ONE_QUEUE	= 0x2000   # ???

def main():
    mode = IFF_TAP | IFF_NO_PI
    TUNSETIFF = 0x400454ca

    tun = os.open("/dev/net/tun", os.O_RDWR)
    ifs = ioctl(tun, TUNSETIFF, struct.pack("16sH", "lvl%d", mode))
    ifname = ifs[:16].strip("\x00")
    os.system("sudo ifconfig %s 192.168.200.1" % ifname)
    print "virtual interface %s created" % ifname
    while True:
        m = mmap.mmap(-1, 1024 * 8) # create in RAM
        s = 'x' * 1024 * 8
        m.write(s)
    	os.write(tun, m)
        print "sent frame"
        time.sleep(1)

if __name__ == '__main__':
    main()