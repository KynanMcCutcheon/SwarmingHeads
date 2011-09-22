'''
Created on Aug 21, 2011

@author: Daniel Grech 16438385
'''

from EventMessage import EventMessage
from swarming_heads.eminterface.CometMessaging import push_message
from swarming_heads.eminterface.Events import EventType
from threading import Thread
import logging
import socket
import sys

class ClientConnection(object):
    '''
    The primary interface to Event Manager. This class has several 
    convenience functions for connecting, disconnecting and sending 
    messages to and from event manager
    '''
    
    def __init__(self, config):
        self.config = config
        self.handler = TcpHandler(self.config.host, self.config.port)
        self.is_connected = False
        
    def send_raw_string(self, str):
        return self.handler.send_string(str)
                
    def connect(self, name, rc=None, re=None, pe=None):
        print 'CONNECTING'
        if self.is_connected:
            logging.info('Attempting to connect a client which is already connected')
            return False, 'This client is already connected'
        
        try:
            #Connect the TCP handler
            self.handler.connect()
            
            #Build & send the connection string
            str = 'MSG EV:' + EventType.NEW + ' NM:' + name
            
            if rc is not None:
                str += EventMessage.MSG_DELIM + EventMessage.RC_TOKEN + EventMessage.PAIR_SEPARATOR + rc
            
            if re is not None:
                str += EventMessage.MSG_DELIM + EventMessage.RE_TOKEN + EventMessage.PAIR_SEPARATOR + re
            
            if pe is not None:
                str += EventMessage.MSG_DELIM + EventMessage.PE_TOKEN + EventMessage.PAIR_SEPARATOR + pe
                
            self.handler.send_string(str)
            
            #Now that we are connected, start a thread to listen for events
            print 'STARTING THE HANDLER THREAD'
            self.handler.start()
        except socket.error, e:
            logging.critical(e.__str__())
            return False, e.__str__()
        else:
            logging.info('Successfully connected to event manager')
            self.is_connected = True
            return True, None

    def disconnect(self):
        if not self.is_connected:
            logging.info("Attempting to disconnect a client which wasn't connected")
            return False, 'This client was not connected'
        
        success, message = self.handler.send_string('MSG EV:' + EventType.DELETE + ' NM:' + self.config.client_name)
        
        if success:
            logging.info('Successfully disconnected from event manager')
            return True, None
        else:
            return False, message
        
class TcpHandler(Thread):   
    '''
    Class to handle the low-level socket connectivity to the Event Manager
    instance. It uses the main application thread to send messages,
    whilst at the same time listens for incoming events in a separate thread
    '''
    
    MAX_LENGTH = 1024;
    
    def __init__(self, h, p):
        Thread.__init__(self, name="TcpHandlerThread")
        self.setDaemon(True)
        self.host = h
        self.port = p
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        #self.lock = Lock()
        
    def __del__(self):
        self.socket.close()
    
    def run(self):        
        while True:       
            try:
                data = self.socket.recv(self.MAX_LENGTH)
                msg = repr(data)            
                logging.info('Received a Message: ' + msg)
                msg = msg.strip("'")
                if not msg.startswith(EventMessage.MSG_HEAD_TOKEN):
                    pass#Comet.push_message(msg)
                    push_message(msg)
            except socket.error, e:
                sys.stderr.write('Error whilst listening for events: ' + e.__str__() + '\n')
                sys.stderr.write('Exiting event listener thread\n')
                
                logging.error(e.__str__())
                logging.error('Exiting event listener thread')
                break
    
    def connect(self):
        self.socket.connect((self.host, self.port))
        self.is_connected = True
    
    def get_header(self, message):
        length = len(message)
        return 'MSGHEAD LEN:' + str(length).zfill(5) + ' PRI:01 TSTAMP: 0000000000000000000'
    
    def send_string(self, string):
        if not self.is_connected:
            logging.error('Attempting to send tcp string before connecting')
            return False, 'TCP Handler is not connected'
        
        try:
            self.socket.sendall(self.get_header(string)) 
            self.socket.sendall(string)
        except socket.error, e:
            logging.error(e.__str__())
            return False, e.__str__()
        else:
            logging.info('TCP string sent: ' + string)
            return True, None
        