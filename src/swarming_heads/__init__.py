from swarming_heads.eminterface.ClientConnection import ClientConnection
from swarming_heads.eminterface.Configuration import Configuration
from swarming_heads.settings import LOG_FILE, LOG_LEVEL, EM_CONFIG_FILE
import logging
import os
import signal
import sys

def setup_logging():
    try:
        logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format='[%(asctime)s/%(levelname)s/%(message)s]')
        logging.info('Logging started')
    except:
        sys.stderr.write('Error setting up logging: ' + str(sys.exc_info()[1]) + ' . Logging may not work\n')


def setup_sighandlers():   
    def handler_sigterm(signum, frame):
        logging.warning("Got a sigterm. Attemping clean exit")
        #Any cleanup tasks here..
        sys.exit(1)
    
    def handler_sigint(signum, frame):
        logging.warning("Got a sigint. Attemping clean exit")
        #Any cleanup tasks here..
        sys.exit(1)
        
    signal.signal(signal.SIGTERM, handler_sigterm)
    signal.signal(signal.SIGINT, handler_sigint)

setup_logging() # Setup logging for the application
setup_sighandlers() # Set up various signal handlers to safely exit the server

# Set up the global singleton to event manager
EM_INTERFACE = None
try:
    config = Configuration(EM_CONFIG_FILE);
    config.load()  
    EM_INTERFACE = ClientConnection(config)
except:
    logging.critical('Error creating event manager interface: ' + str(sys.exc_info()[1]) + '. Exiting..')
    sys.exit(1)