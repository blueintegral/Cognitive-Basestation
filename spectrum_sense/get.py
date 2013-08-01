import get_channels.py
import pymongo

from pymongo import Connection
connection = Connection()
db = connection.clientDB
clients = db.clients

def users():
	#return the number of users camped to this base station
	return clients.count()	

def channels():
	#return vector of available channels
	return get_channels.areOpen()

def total_interference():
	#return total interference from all clients
	

def currentChannelAssignment():
	#return vector of all client IDs and their assigned channel
	
