import eventlet
from eventlet.greenpool import GreenPool
import time

pool = GreenPool(10)

samples = range(0,100)  

def send_data(sample):
    print "num running:",pool.free()
    #eventlet.sleep(10)
    print sample

def consume_samples(samples):
    [result for result in pool.imap(send_data,samples)]



consume_samples(samples)
