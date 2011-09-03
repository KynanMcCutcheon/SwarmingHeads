from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from stompservice.client import StompClientFactory
from subprocess import CalledProcessError
from swarming_heads.Util import Util
from swarming_heads.settings import RPC_SERVER_HOST, RPC_SERVER_PORT, STOMP_HOST, \
    STOMP_PORT, ORBITED_START_COMMAND
from threading import Thread
from twisted.internet.selectreactor import SelectReactor
import exceptions
import logging
import os
import simplejson
import subprocess
import sys
import xmlrpclib

class CometMessageSender(StompClientFactory):
    def recv_connected(self, msg):
        logging.info('Comet message sender registered')

    def send_data(self, channel, data):
        logging.info("Sending data '" + data + "' to channel '" + channel + "'")
        # modify our data elements
        
        to_send = simplejson.JSONEncoder().encode(data)

        try:
            self.send(channel, to_send)
        except exceptions.AttributeError as e:
            logging.error('Error sending data: ' + str(e))

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class RPCServer(Thread):
    def __init__(self, orbited):
        Thread.__init__(self, name="RPCServerThread")
        self.setDaemon(True)
        self.orbited = orbited
        self.host = RPC_SERVER_HOST
        self.port = RPC_SERVER_PORT
        
    def run(self):
        #create a server
        server = SimpleXMLRPCServer((self.host, self.port),
                                    requestHandler = RequestHandler)

        server.register_introspection_functions()
        
        def transmit_orbited(channel, message):
            self.orbited.send_data(channel, message)
            return ""

        server.register_function(transmit_orbited, 'transmit')
        server.serve_forever()

class OrbitedServer(Thread):
    def __init__(self):
        Thread.__init__(self, name="OrbitedServerThread")
        self.setDaemon(True)
        self.start_command = ORBITED_START_COMMAND
    
    def run(self):
        try:
            devnull = open(os.devnull,"w")
            subprocess.check_call(self.start_command, stdout=devnull, stderr=devnull)
            devnull.close()
        except CalledProcessError as e:
            logging.critical('Error running orbited server. ' + str(e) + ' Exiting..')
            Util.clean_exit(1)
        except:
            logging.critical('Unknown critical error ' + str(sys.exc_info()[1]))
            Util.clean_exit(1)

class Comet(Thread):
    def __init__(self):
        Thread.__init__(self, name="CometThread")
        self.setDaemon(True)
        #self.orbited_server = OrbitedServer()
        self.orbited_proxy = CometMessageSender()
        self.rpcthread = RPCServer(self.orbited_proxy)
        self.host = STOMP_HOST
        self.port = STOMP_PORT

    def run(self):
        #self.orbited_server.start()
        self.rpcthread.start()

        r = SelectReactor()
        r.connectTCP(self.host, self.port, self.orbited_proxy)
        r.run(installSignalHandlers=0)
        
    def __del__(self):
        pass
      
    RPC_PROXY = xmlrpclib.ServerProxy('http://' + RPC_SERVER_HOST + ':' + str(RPC_SERVER_PORT))  
    
    @staticmethod  
    def push_message(message):
        try:
            Comet.RPC_PROXY.transmit("/topic/shouts", message)
        except xmlrpclib.Fault as e:
            logging.error('Error transmitting message: ' + e)
        except:
            logging.error('Unknown error occured: ' + e)
        
