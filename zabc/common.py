import logging
import os
import logging.config
from logger import logger
logging.setLoggerClass(logger.ZbcLogger)
log = logging.getLogger("zabc")

# Create log file
loglevel = 'DEBUG'
logfile = '/var/log/zabc/zabc.log'
if not os.path.isdir(os.path.dirname(logfile)):
    os.makedirs(os.path.dirname(logfile))
logging.config.fileConfig("/etc/zabc/logging.cfg",defaults={'loglevel': loglevel, 'logfile': logfile})


#Transfer item key
def transfer_item_key(item_key):
    '''
     Some item_key will be change ,for example 
     cpu is now change cpu.time
     memory is change memory.total
    '''
    if item_key == 'cpu':
        item_key = 'cpu.time'
    elif item_key == 'cpu_util':
        item_key = item_key
    elif item_key == 'memory':
        item_key = 'memory.total'
    elif item_key == 'memory_usage':
        item_key = item_key
    elif 'rate' in item_key:
        item_key = item_key
    else:
        item_key = item_key+'.total'
    return item_key
