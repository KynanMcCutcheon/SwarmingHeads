'''
Created on Sep 22, 2011

@author: daniel
'''
from swarming_heads.settings import HOOKBOX_HOST, HOOKBOX_PORT
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
    
    print 'BRO IM PUSHING A MESSAGE'
    
    url = "http://" + HOOKBOX_HOST + ":" + HOOKBOX_PORT + "/rest/publish"
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    urllib2.urlopen(req)