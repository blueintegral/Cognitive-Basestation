#!/usr/bin/python
#/usr/bin/env python

from pymongo import Connection
connection = Connection()
db = connection.clientDB
client = db.clients

client1 = {"clientID": "0001",
	   "frequency": "521",
	   "bandwidth": "6",
	   "interference": "1.2"}

client2 = {"clientID": "0002",
	   "frequency": "527",
	   "bandwidth": "6",
	   "interference": "0.5"}

client3 = {"clientID": "0003",
	   "frequency": "533",
	   "bandwidth": "6",
	   "interference": "1.8"}


client.insert(client1)
client.insert(client2)
client.insert(client3)

