from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from stompservice.client import StompClientFactory
from swarming_heads.settings import RPC_SERVER_HOST, RPC_SERVER_PORT, \
    ORBITED_HOST, ORBITED_PORT
from threading import Thread
from twisted.internet.selectreactor import SelectReactor
import exceptions
import logging
import simplejson

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
        
class Comet(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.orbited_proxy = CometMessageSender()
        self.rpcthread = RPCServer(self.orbited_proxy)

    def run(self):
        self.rpcthread.start()
        r = SelectReactor()
        r.connectTCP(ORBITED_HOST, ORBITED_PORT, self.orbited_proxy)
        r.run(installSignalHandlers=0)
