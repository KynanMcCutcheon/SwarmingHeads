from swarming_heads.apps.testing.Comet import Comet
from swarming_heads.settings import LOG_FILE, LOG_LEVEL
import logging
import sys

#Setup logging for the application
try:
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
except:
    sys.stderr.write('Error setting up logging: ' + sys.exc_info()[0] + ' . Logging may not work\n')

try:
    logging.info('Starting comet server')
    c = Comet()
    c.start()
    logging.info('Comet server running')
except:
    logging.critical('Error starting up the comet server: ' + sys.exc_info()[0] \
                     + '. Exiting server..')
    sys.exit(1)
    