from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from stompservice import client
from stompservice.client import StompClientFactory
from threading import Thread
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import exceptions
import simplejson


class DataProducer(StompClientFactory):
    def recv_connected(self, msg):

        print 'Connected; producing data'

        # the next two lines are probably the biggest workaround
        # for the weirdest bug I've seen in my entire life
        # it repeatedly calls a function that absolutely does nothing
        # however, if I remove them, there's a ten second delay
        # between when the DataProducer transmits a message to
        # when the browser actually receives the data. Me and my
        # friend were mindfucked thinking about how something like
        # this could possibly happen. But right now we are more worried
        # about the rest of the code
        #self.timer = LoopingCall(self.test_data)
        #self.timer.start(INTERVAL/1000.0)

    def send_data(self, channel, data):
        print "Transmitting: ", channel, data
        # modify our data elements
        to_send = simplejson.JSONEncoder().encode(data)
        print 'DATA TO SEND', to_send
        try:
            self.send(channel, to_send)
        except exceptions.AttributeError as e:
            print 'QQ', e

    def test_data(self):
        pass

orbited_proxy = DataProducer()

class RPCServer(Thread):
    def __init__(self, orbited):
        self.orbited = orbited
        Thread.__init__(self)
    def run(self):
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/RPC2',)
        #create a server
        server = SimpleXMLRPCServer(("127.0.0.1",8045),
                                    requestHandler = RequestHandler)

        server.register_introspection_functions()
        def transmit_orbited(channel, message):
            """
            @param channel: The stomp channel to send to
            @param message: The message that needs to be transmitted
            """
            self.orbited.send_data(channel, message)
            return ""

        server.register_function(transmit_orbited, 'transmit')
        server.serve_forever()

rpcthread = RPCServer(orbited_proxy)
rpcthread.start()


reactor.connectTCP('127.0.0.1', 61613, orbited_proxy)
reactor.run()