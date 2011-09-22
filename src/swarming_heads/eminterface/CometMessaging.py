'''
Created on Sep 22, 2011

@author: daniel
'''
from swarming_heads.settings import HOOKBOX_HOST, HOOKBOX_PORT
import json
import logging
import random
import urllib
import urllib2

def push_message(message):
    '''
    ROBOT -- > USER communication
    
    Static method which will push data from the server to the browser
    '''
    values = { "secret" : "secret",
               "channel_name" : "/chat/",
               "payload" : []
             }
    
    logging.info("pushing message: " + message)
    
    values["payload"] = json.dumps(message)
        
    url = "http://" + HOOKBOX_HOST + ":" + str(HOOKBOX_PORT) + "/rest/publish"
    print url    
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)
    print resp.read()