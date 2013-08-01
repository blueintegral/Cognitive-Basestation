#!/usr/bin/python
#!/usr/bin/env python

#This file launches spectrum_sense.py in one thread and transactions.py in another thread. This file should be executed to start the basestation.

import os
import threading

def start_transactions:
    os.system('./transactions.py')
    print 'Transactions started sucessfully'

def start_spectrum_sense:
    os.system('./spectrum_sense.py')
    print 'Spectrum sensing started sucessfully'

t1 = Thread(start_spectrum_sense)
t2 = Thread(start_transactions)

t1.start()
t2.start()



