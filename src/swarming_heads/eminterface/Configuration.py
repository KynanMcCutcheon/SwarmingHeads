'''
Created on Aug 21, 2011

@author: Daniel Grech 16438385
'''
import ConfigParser
import random

class Configuration(object):
    '''
    Class which parses and initializes the program based on values
    found in a config file. This class also defines some defaults if 
    values cannot be found in the config file
    '''
    
    #The different sections in the config file
    SECTION_CONNECTION_DETAILS = 'Connection_Details'
    SECTION_CLIENT_DETAILS = 'Client_Details'
    SECTION_DEBUG = 'Debug'
    
    #The different config options to be found in a config file
    OPTION_HOST = 'Host'
    OPTION_PORT = 'Port'
    OPTION_LOGFILE = 'Logfile'
    OPTION_LOGLEVEL = 'LogLevel'
    OPTION_CLIENT_NAME = 'ClientName'
    
    #Default configuration values if not found in the config file
    DEFAULT_CONFIG_FILE = 'client.cfg'
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 30001
    DEFAULT_LOGFILE = 'client.log'
    DEFAULT_LOGLEVEL = 'WARNING'
    DEFAULT_CLIENT_NAME = 'client' + str(random.randint(1,100))
    
    #A dictionary which specifies default values should they 
    #be missing in the config file
    DEFAULT_CONFIG_DICT = {OPTION_HOST : DEFAULT_HOST,
                           OPTION_PORT : DEFAULT_PORT,
                           OPTION_LOGFILE : DEFAULT_LOGFILE,
                           OPTION_LOGLEVEL : DEFAULT_LOGLEVEL,
                           OPTION_CLIENT_NAME : DEFAULT_CLIENT_NAME  }
    
    def __init__(self, cf = DEFAULT_CONFIG_FILE):
        self.config = ConfigParser.SafeConfigParser(self.DEFAULT_CONFIG_DICT)
        self.config_file = cf
    
    def load(self):
        self.config.read(self.config_file)
       
        self.host = self.config.get(self.SECTION_CONNECTION_DETAILS, self.OPTION_HOST)
        self.port = self.config.getint(self.SECTION_CONNECTION_DETAILS, self.OPTION_PORT)
        self.logfile = self.config.get(self.SECTION_DEBUG, self.OPTION_LOGFILE)
        self.loglevel = self.config.get(self.SECTION_DEBUG, self.OPTION_LOGLEVEL)
        self.client_name = self.config.get(self.SECTION_CLIENT_DETAILS, self.OPTION_CLIENT_NAME)