'''
Created on Sep 22, 2011

@author: daniel
'''
from EventMessage import EventMessage
from swarming_heads.eminterface.EventMessage import EventMessageBuilder
from swarming_heads.eminterface.Events import EventType, EventList, ErrorList
from swarming_heads.settings import HOOKBOX_HOST, HOOKBOX_PORT
import json
import logging
import urllib
import urllib2

def push_error_message(message, username):
    #Construct our message for EventManager
    builder = EventMessageBuilder()
    
    builder.event_type = EventType.ERROR
    builder.event_name = ErrorList.ERROR_UNKNOWN
    builder.client_name = username
    
    #Get robot name from database based on the username above
    # builder.event_destination = Database.getRobotNameFromUser(builder.client_name)
    builder.event_destination = 'client1'
    
    builder.event_content = EventMessage.MSG_ARG_DELIM + message + EventMessage.MSG_ARG_DELIM
    push_message(builder.build().toString(), username)

def push_message(message, username):
    '''
    ROBOT -- > USER communication
    
    Static method which will push data from the server to the browser
    '''
    values = { "secret" : "secret",
               "channel_name" : username,
               "payload" : []
             }
    
    logging.info("pushing message: " + message)
    
    jsonMsg = EventMessage.toJSON(message)
    
    if jsonMsg is not None:
        values["payload"] = jsonMsg
    else:
        values["payload"] = json.dumps(message)
        
    url = "http://" + HOOKBOX_HOST + ":" + str(HOOKBOX_PORT) + "/rest/publish"
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)