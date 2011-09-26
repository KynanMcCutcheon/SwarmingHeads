from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from swarming_heads.eminterface.ClientConnection import ClientConnection
from swarming_heads.eminterface.CometMessaging import push_error_message
from swarming_heads.eminterface.EventMessage import EventMessageBuilder, \
    EventMessage
from swarming_heads.eminterface.Events import EventType, EventList
from swarming_heads.settings import EM_HOST, EM_PORT
import json
import logging
import sys

@csrf_exempt
def connect(request):
    
    logging.debug("Connecting")
    
    jsonString = json.dumps([ True, {"name" : "daniel" } ])
    
    return HttpResponse(content=jsonString, status=200)
    
    
@csrf_exempt
def create_channel(request):
    
    logging.debug("Creating channel")
    jsonString = json.dumps([ True, { "history_size" : 0, 
                                    "reflective" : True, 
                                    "presenceful" : True } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def subscribe(request):
    
    logging.debug("Creating subscription")
    jsonString = json.dumps([ True, {  } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def disconnect(request):
    
    logging.debug("Disconnecting client")
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)


@csrf_exempt
def publish(request):
    '''
    USER -- > ROBOT communication
    
    Handler to receive message from Browser and pass along to client robot
    '''
    print 'IM HERE MAN'
    
    em_connection = request.session.get('em_connection', None)
    
    if em_connection is None:
        try:
            em_connection = ClientConnection(EM_HOST, EM_PORT)
        except :
            print 'GOING TO SEND ERROR MESSAGE'
            logging.warning("Couldnt initialize to event manager: " + str(sys.exc_info()[1]))
            push_error_message('Error initializing to event manager: ' + str(sys.exc_info()[1]), request.user.username)
            return HttpResponse(content=json.dumps([ True, {} ]), status=200)
    
    if not em_connection.is_connected:           
        success, err_msg = em_connection.connect(request.user.username)
        if not success:
            print 'GOING TO SEND ERROR MESSAGE'
            logging.warning("Couldnt connect to event manager: " + err_msg)
            push_error_message('Error connecting to event manager: ' + err_msg, request.user.username)
            return HttpResponse(content=json.dumps([ True, {} ]), status=200)
    
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

    success, err_msg = em_connection.send_raw_string(builder.build().toString())
    
    if not success:
        # Send error message to client!
        logging.warning("ERROR SENDING MESSAGE " + err_msg)
        jsonString = json.dumps([ False, {"Error" : err_msg} ])
    else:
        jsonString = json.dumps([ True, {} ])
    
    
    return HttpResponse(content=jsonString, status=200)
    