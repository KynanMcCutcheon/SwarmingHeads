from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from stompservice.client import StompClientFactory
from subprocess import CalledProcessError
from swarming_heads.settings import RPC_SERVER_HOST, RPC_SERVER_PORT, STOMP_HOST, \
    STOMP_PORT, ORBITED_CONFIG_FILE
from threading import Thread
from twisted.internet.selectreactor import SelectReactor
import exceptions
import logging
import simplejson
import subprocess
import sys

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
            logging.error('Error sending data: ' + e)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class RPCServer(Thread):
    def __init__(self, orbited):
        Thread.__init__(self)
        self.setDaemon(True)
        self.orbited = orbited
        
    def run(self):
        #create a server
        server = SimpleXMLRPCServer((RPC_SERVER_HOST,RPC_SERVER_PORT),
                                    requestHandler = RequestHandler)

        server.register_introspection_functions()
        
        def transmit_orbited(channel, message):
            self.orbited.send_data(channel, message)
            return ""

        server.register_function(transmit_orbited, 'transmit')
        server.serve_forever()

class OrbitedServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.orbited_command = ['orbited', '--config=' + ORBITED_CONFIG_FILE ]
    
    def run(self):
        try:
            subprocess.check_call(self.orbited_command)
        except CalledProcessError as e:
            logging.critical('Error running orbited server. Exiting..')
            sys.exit(1)

class Comet(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.orbited_server = OrbitedServer()
        self.orbited_proxy = CometMessageSender()
        self.rpcthread = RPCServer(self.orbited_proxy)

    def run(self):
        self.orbited_server.start()
        self.rpcthread.start()
        r = SelectReactor()
        r.connectTCP(STOMP_HOST, STOMP_PORT, self.orbited_proxy)
        r.run(installSignalHandlers=0)
