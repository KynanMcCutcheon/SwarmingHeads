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

def getEmConnection(username):
    try:
        em_connection = ClientConnection(EM_HOST, EM_PORT)     
        success, err_msg = em_connection.connect(username)
        if not success:
            logging.warning("Couldnt connect to event manager: " + err_msg)
            return None
        
        return em_connection
    except :
        logging.warning("Couldnt initialize to event manager: " + str(sys.exc_info()[1]))
        return None

@csrf_exempt
def connect(request):
    logging.debug("Connecting")
    em_connection = getEmConnection(request.user.username)
    if em_connection is None:
        return HttpResponse(content=json.dumps([ False, {"name" : request.user.username} ]), status=200)
    else:
        logging.debug('Adding new em_connection to thread pool for user: ' + request.user.username)
        ThreadPool.add(request.user.username, em_connection)

    jsonString = json.dumps([ True, {"name" : request.user.username } ])
    
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
    
    ThreadPool.remove(request.user.username)
    
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)


@csrf_exempt
def publish(request):
    '''
    USER -- > ROBOT communication
    
    Handler to receive message from Browser and pass along to client robot
    '''    
    
    em_connection = ThreadPool.get(request.user.username)
    
    if em_connection is None:
        logging.debug('No em_connection in pool by user: ' + request.user.username)
        em_connection = getEmConnection(request.user.username)
        if em_connection is None:
            return HttpResponse(content=json.dumps([ True, {} ]), status=200)
        else:
            logging.debug('Adding new connection to pool in publish for user: ' + request.user.username)
            ThreadPool.add(request.user.username, em_connection)
    else:
        logging.debug('Got em_connection from pool for user ' + request.user.username)
    #else:
        #request.session['em_connecton'] = em_connection
    
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

class ThreadPool(object):
    '''
    Simple wrapper class to hold references to all 
    connections between web app and event manager
    '''
    pool = {}
    
    @staticmethod
    def add(name, thread):
        ThreadPool.pool[name] = thread
    
    @staticmethod
    def get(name):
        return ThreadPool.pool.get(name, None)
        
    @staticmethod
    def remove(name):
        ThreadPool.pool.pop(name, None)
        
    
    
    