#!/usr/bin/python
#!/usr/bin/env python
#
import time
import os
import numpy
from subprocess import call
import urllib2
from xml.dom.minidom import parseString

#To do: after getting the available channels back from spectrum bridge, inspect them 
#ourselves to make sure they're free. Also, add a flag that will check for other open
#channels as well, even if spectrum bridge says they're not free, because they often are.

unbounded_search = False #Set this to True if you want to search ALL channels, not just the ones that spectrum bridge says are free. Often, channels marked used are really free, however using them is technically illegal.

#The index of the dictionary below is the channel number and the number at that index is the frequency in MHz. If it's 0, then that channelisn't allocated.
channels = [0, 0, 54, 60, 66, 76, 82, 174, 180, 186, 192, 198, 204, 210, 470, 476, 482, 488, 494, 500, 506, 512, 518, 524, 530, 536, 542, 548, 554, 560, 566, 572, 578, 584, 590, 596, 602, 608, 614, 620, 626, 632, 638, 644, 650, 656, 662, 668, 674, 680, 686, 692, 698, 704, 710, 716, 722, 728, 734, 740, 746, 752, 758, 764, 770, 776, 782, 788, 794, 800, 806, 812, 818, 824, 830, 836, 842, 848, 854, 860, 866, 872, 878, 884]
 #FIXME You're supposed to use the requests library for this, but I couldn't get it to work. 
opener = urllib2.build_opener(urllib2.HTTPHandler)
request = urllib2.Request('https://tvws-demo.spectrumbridge.com/v3/devices/US/MGNFCCID001/100', data='<RegistrationRequest xmlns="http://schemas.datacontract.org/2004/07/SpectrumBridge.WhiteSpaces.Services.v3"><AntennaHeight>1</AntennaHeight><ContactCity>Sunnyvale</ContactCity><ContactCountry>US</ContactCountry><ContactEmail>matt@meownetworks.com</ContactEmail><ContactName>Matt</ContactName><ContactPhone>4077621500</ContactPhone><ContactState>CA</ContactState><ContactStreet>1011 Rosa Avenue</ContactStreet><ContactZip></ContactZip><DeviceOwner>Matt</DeviceOwner><DeviceType>8</DeviceType><Latitude>28.00000</Latitude><Longitude>-81.00000</Longitude></RegistrationRequest>')
request.add_header('Content-Type', 'Application/xml')
request.get_method = lambda: 'PUT'
url = opener.open(request)
try: resp = urllib2.urlopen('https://tvws-demo.spectrumbridge.com/v3/channels/US/28.00000/-81.00000/?fccid=MGNFCCID001&serial=100&type=8&ant=1')
except URLError, e:
    print e.reason
    print e.code
    print e.read()
#   print resp.info()
#   print resp.read()

#Do some string ops to extract the available channels from the response
response = resp.read()
dom = parseString(response)
xmlTag = dom.getElementsByTagName('ChannelCount')[0].toxml()
xmlData = xmlTag.replace('<ChannelCount>','').replace('</ChannelCount>','')
ChannelCount = xmlData
xmlTag = dom.getElementsByTagName('ChannelList')[0].toxml()
xmlData = xmlTag.replace('<ChannelList>','').replace('</ChannelList>','')
ChannelList = xmlData
xmlTag = dom.getElementsByTagName('RefreshIn')[0].toxml()
xmlData = xmlTag.replace('<RefreshIn>','').replace('</RefreshIn>','')
RefreshIn = xmlData
print "Channel Count: ", ChannelCount
print "Channel List: ", ChannelList
print "Refresh In: ", RefreshIn
ChannelList = [int(i) for i in ChannelList.split(',')]
for i in numpy.arange(1, len(ChannelList), 1):
   # print ChannelList[i]
    print "Now scanning channel", ChannelList[i],
    print "which has a frequency of", channels[ChannelList[i]],
    print "MHz"
    time.sleep(2)
    #FIXME This is not the right way to call this script. Should be imported and done the right way.
    os.system('./usrp_spectrum_sense.py '+str(channels[ChannelList[i]])+'M'+' '+str((channels[ChannelList[i]]+6))+'M')
if (unbounded_search):
	print "#######################################"
	print "Preparing for complete spectral scan. Last chance to abort, cause this could take a while."
	print "#######################################"
	time.sleep(5)
	for j in numpy.arange(1, len(channels), 1):
		print "Now scanning", channels[j],
		print "MHz"
		time.sleep(2)
		#FIXME This is not the right way to call this script. Should be imported and done theright way.
		os.system('./usrp_spectrum_sense.py '+str(channels[j])+'M'+' '+str(channels[j]+6)+'M')

def areOpen():
	return ChannelList

 
