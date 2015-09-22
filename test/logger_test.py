#!/usr/bin/env python
import os
import sys
import logging
import logging.config
from logger import logger
logging.setLoggerClass(logger.ZbcLogger)

log = logging.getLogger("zbc")

logname = 'mylogtest.log'
defaults = {
    'loglevel'   : 'DEBUG',
    'logfile'    : os.path.join('{storedir}', 'logs', logname),
    'log_config' : os.path.join('{logdir}', 'logger', 'logging.cfg'),
}
# Create log file

loglevel = defaults['loglevel']
logfile = defaults['logfile'].format(storedir="/var/log")
log_config = defaults['log_config'].format(logdir="/root/Zabbix_Ceilometer/zabbix_ceilometer_plugin")
if not os.path.isdir(os.path.dirname(logfile)):
    os.makedirs(os.path.dirname(logfile))

logging.config.fileConfig(log_config,defaults={'loglevel': loglevel, 'logfile': logfile})

def main():
    # Define except hook to redirect all erros to file
    sys.excepthook = lambda tp, v, tb: log.error('ERROR', exc_info=(tp,v,tb))
    try:
        raise("big error!")
    except:
        log.error('** Packager Failed **')
        print "aaaa"
    else:
        log.info("bbb")
    finally:
        log.info("ccc")
    print "aaaaaa"
    import pdb;pdb.set_trace()
    log.reprint_errors()
# ** MAIN **

if __name__ == '__main__':
    main()

