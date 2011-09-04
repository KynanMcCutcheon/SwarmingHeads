from ClientConnection import ClientConnection
from Configuration import Configuration
from EventMessage import EventMessage
from swarming_heads.eminterface.EventMessage import EventMessageBuilder
from swarming_heads.eminterface.Events import EventType, EventList
import logging
import sys

if __name__ == '__main__':        
    
    #Get a new Configuration instance
    config = Configuration('../em_interface.cfg');
    
    #Load parameters from the config file
    config.load()  
    
    #Setup logging for the application
    numeric_log_level = getattr(logging, config.loglevel.upper(), None)
    logging.basicConfig(filename=config.logfile,level=numeric_log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    #Get a new client instance    
    client = ClientConnection(config)
    
    #Initiate a connection between the client and the event manager.
    success, err_msg = client.connect()
    if not success:
        sys.stderr.write('Error connecting to event manager: ' + err_msg + '\n')
        sys.exit(1)
    
    #Write 5 messages
    for i in range(5):
        msg = raw_input("Enter a message to send: ")
        builder = EventMessageBuilder()
        builder.event_type = EventType.EVENT
        builder.event_name = EventList.TEXT_MESSAGE
        builder.client_name = config.client_name
        builder.event_destination = 'client1'
        builder.event_content = msg
        success, err_msg = client.send_raw_string(builder.build().toString())
        
        if not success:
            sys.stderr.write('Error sending message to event manager: ' + err_msg + '\n')
    
    #Disconnect from the client
    success, err_msg = client.disconnect()
    
    if not success:
        sys.stderr.write('Error disconnecting from event manager: ' + err_msg + '\n')
        sys.exit(1)
        