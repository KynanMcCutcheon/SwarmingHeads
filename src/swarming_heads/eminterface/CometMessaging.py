'''
Created on Sep 22, 2011

@author: daniel
'''
from swarming_heads.settings import HOOKBOX_HOST, HOOKBOX_PORT
from EventMessage import EventMessage
import json
import logging
import urllib
import urllib2

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