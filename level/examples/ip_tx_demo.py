#! /usr/bin/python

import socket, time

def send_udp(ip, port, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto(msg, (ip, port))
	print "sent", msg

def send_tcp(ip, port, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
	sock.connect((ip, port))
	sock.send(msg)
	print "sent", msg

if __name__ == '__main__':
	ip = "127.0.0.1"
	port = 8000
	msg = "Hello, World!"
	while True:
		#send_udp(UDP_IP, UDP_PORT, MESSAGE)
		send_tcp(ip, port, msg)
		time.sleep(2)