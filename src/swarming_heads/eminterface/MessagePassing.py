'''
Created on Sep 22, 2011

@author: daniel
'''
from django.http import HttpResponse
from swarming_heads import EM_INTERFACE
from swarming_heads.eminterface.EventMessage import EventMessageBuilder, \
    EventMessage
from swarming_heads.eminterface.Events import EventType, EventList
from swarming_heads.settings import HOOKBOX_HOST, HOOKBOX_PORT
import json
import logging
import urllib
import urllib2


def push_message(message):
    '''
    ROBOT -- > USER communication
    
    Static method which will push data from the server to the browser
    '''
    values = { "channel_name" : "/chat/",
               "payload" : message
             }
    
    url = "http://" + HOOKBOX_HOST + ":" + HOOKBOX_PORT + "/rest/publish"
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    urllib2.urlopen(req)
    
def send_message(request):
    '''
    USER -- > ROBOT communication
    
    Handler to receive message from Browser and pass along to client robot
    '''
     
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