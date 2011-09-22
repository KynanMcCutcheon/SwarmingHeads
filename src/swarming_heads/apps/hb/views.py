from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from swarming_heads.eminterface.Configuration import Configuration
from swarming_heads.eminterface.EventMessage import EventMessageBuilder, \
    EventMessage
from swarming_heads.eminterface.Events import EventType, EventList
from swarming_heads.settings import EM_CONFIG_FILE, EM_INTERFACE, HOOKBOX_HOST, \
    HOOKBOX_PORT
import json
import logging
import sys
import urllib
import urllib2

@csrf_exempt
def connect(request):
    
    print 'CONNECTING BRO'
    if EM_INTERFACE is None:
        try:
            config = Configuration(EM_CONFIG_FILE);
            config.load()  
            EM_INTERFACE = ClientConnection(config)
        except:
            logging.critical('Error creating event manager interface: ' + str(sys.exc_info()[1]) + '. Exiting..')
            sys.exit(1)

    
    if not EM_INTERFACE.is_connected:
        success, err_msg = EM_INTERFACE.connect(request.user.username)
        print "CONNECTED TO EVENT MANAGER"
    if not success:
        print "COULDNT CONNECT TO EVENT MANAGER " + err_msg #Comet.push_message('Error connecting to event manager: ' + err_msg)
    
    
    jsonString = json.dumps([ True, { "name" : "daniel" } ])
    
    return HttpResponse(content=jsonString, status=200)
    
    
@csrf_exempt
def create_channel(request):
    
    print 'CREATING CHANNEL BRO'
    jsonString = json.dumps([ True, { "history_size" : 0, 
                                    "reflective" : True, 
                                    "presenceful" : True } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def subscribe(request):
    
    print 'SUBSCRIBING BRO'
    jsonString = json.dumps([ True, {  } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def disconnect(request):
    
    print 'DISCONNECTING BRO'
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)


@csrf_exempt
def publish(request):
    return send_message(request)

def push_message(message):
    '''
    ROBOT -- > USER communication
    
    Static method which will push data from the server to the browser
    '''
    values = { "channel_name" : "/chat/",
               "payload" : message
             }
    
    print 'BRO IM PUSHING A MESSAGE'
    
    url = "http://" + HOOKBOX_HOST + ":" + HOOKBOX_PORT + "/rest/publish"
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    urllib2.urlopen(req)
    
def send_message(request):
    '''
    USER -- > ROBOT communication
    
    Handler to receive message from Browser and pass along to client robot
    '''
    if EM_INTERFACE is None:
        try:
            config = Configuration(EM_CONFIG_FILE);
            config.load()  
            EM_INTERFACE = ClientConnection(config)
        except:
            logging.critical('Error creating event manager interface: ' + str(sys.exc_info()[1]) + '. Exiting..')
            sys.exit(1) 
     
    if not EM_INTERFACE.is_connected:
        success, err_msg = EM_INTERFACE.connect(request.user.username)
        if not success:
            logging.warning("COULDNT CONNECT TO EVENT MANAGER " + err_msg)#Comet.push_message('Error connecting to event manager: ' + err_msg)
    
    if request.POST.has_key('payload'):
        message = request.POST['payload']
    else:
        logging.warning('Couldnt find payload in POST request')
        
    if request.POST.has_key('action'):
        action = request.POST['action']
    else:
        logging.warning('Couldnt find action in POST request')
        
    if request.POST.has_key('channel_name'):
        channel = request.POST['channel_name']
    else:
        logging.warning('Couldnt find channel name in POST request')


    if channel != request.user.username:
        logging.warning("User not accessing own channel .. should block here!")


    #Construct our message for EventManager
    builder = EventMessageBuilder()
    
    builder.event_type = EventType.EVENT
    builder.event_name = EventList.TEXT_MESSAGE
    builder.client_name = request.user.username
    
    #Get robot name from database based on the username above
    # builder.event_destination = Database.getRobotNameFromUser(builder.client_name)
    builder.event_destination = 'client1'
    
    builder.event_content = EventMessage.MSG_ARG_DELIM + message + EventMessage.MSG_ARG_DELIM

    success, err_msg = EM_INTERFACE.send_raw_string(builder.build().toString())
    
    if not success:
        # Send error message to client!
        logging.warning("ERROR SENDING MESSAGE " + err_msg)#Comet.push_message('Error sending message: ' + err_msg)
        jsonString = json.dumps([ False, {} ])
    else:
        jsonString = json.dumps([ True, {} ])
    
    
    return HttpResponse(content=jsonString, status=200)