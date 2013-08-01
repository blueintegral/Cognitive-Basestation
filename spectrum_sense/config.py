from pymongo import Connection
connection = Connection()
db = connection.clientDB
client = db.clients


def changeChannel(user, freq):
	#return true or false if sucessful at changing given user to given channel
	client.update(
		{ 'ClientID':user},
		{ 'frequency':freq}
	)
	#FIXME After updating the database, command the client to new parameters
