#!/usr/bin/python
#/usr/bin/env python
#
import math
import get
import config
random.seed()

#
#This script will do channel selection based on interference. It approximates a
#Nash equilibrium via simulated annealing. It will always find an good approximation to 
#a Nash equilibrium in polynomial time, but it probably won't achieve Pareto optimality
#very often.


n = get.users() #Number of users.
max = length(get.channels()) #Number of channels available.
z = [0] * n #This will hold the channel assignment solution
T = 100 #Initial temperature. 100 was chosen emperically.
i = 0
iterations = 12 #A formula for getting this number should be derived emperically
total_interference = get.totalInterference() #Interference of all users.

#FIXME Do something more intelligent than just randomly changing channels around

while (i < iterations):
	c = random.randrange(1,max) #pick a random channel that's open
	u = random.randrange(1,n) #pick a random user
	config.change_channel(u, c) #assign that channel to that user
	new_total_interference = get.totalInterference()
	delta_I = total_interference - new_total_interference
	if (delta_I > 0):
		# z = get.currentChannelAssignment()
		total_interference = new_total_interference
	else
		p = rand(1,0)
		if (p < exp(-(delta_I)/T)):
			# z = get.currentChannelAssignment()
			total_interference = new_total_interference
	T = T*0.8 #Decrease temperature. 0.8 was chosen emperically.
	i = i + 1
#print z

