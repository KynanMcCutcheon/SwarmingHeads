'''
Created on Aug 21, 2011

@author: Daniel Grech 16438385

@summary: 
'''
import json
import logging

class EventMessage(object):
    '''
    Represents a single event message passed between a client
    and the event manager. Has several convenience functions to
    aid in parsing raw message strings into usable objects
    '''
    
    MSG_SPACE_SUB = '<%_>'    
    PAIR_SEPARATOR = ':'
    MSG_DELIM = ' '
    MSG_ARG_DELIM = '*'
    MSG_TOKEN = 'MSG '
    MSG_HEAD_TOKEN = 'MSGHEAD'
    EV_TOKEN = 'EV'
    NM_TOKEN = 'NM'
    EN_TOKEN = 'EN'
    EC_TOKEN = 'EC'
    TC_TOKEN = 'TC'
    RC_TOKEN = 'RC'
    RE_TOKEN = 'RE'
    PE_TOKEN = 'PE'
    
    def __init__(self, ev, nm, en, ec, tc, rc, re, pe):
        self.event_type = ev
        self.client_name = nm
        self.event_name = en
        self.event_content = ec
        self.event_destination = tc
        self.need_client = rc
        self.need_event = re
        self.provide_event = pe
        
        logging.debug('ev=%s, nm=%s, en=%s, ec=%s, tc=%s, rc=%s, re=%s, pe=%s', 
                      ev, nm, en, ec, tc, rc, re, pe) 
    
    @classmethod
    def fromString(cls, str):
        if not str.startswith(' '):
            str = ' ' + str

        #Before we split by space, make sure our message doesn't contain any..
        start = str.find('*')
        end = str.rfind('*')
        original = str[start:end+1]
        str = str.replace(original, original.replace(' ', cls.MSG_SPACE_SUB))
    
        #Split the string by space character
        token_list = str.split(cls.MSG_DELIM)
    
        #Initialize our answers
        ev = None
        nm = None
        en = None
        ec = None
        tc = None
        rc = None
        re = None
        pe = None
    
        #Find all the values that we can   
        for token in token_list:
            key, _, value = token.partition(cls.PAIR_SEPARATOR)
            
            if key == cls.EV_TOKEN:
                ev = value                
            elif key == cls.NM_TOKEN:
                nm = value
            elif key == cls.EN_TOKEN:
                en = value
            elif key == cls.EC_TOKEN:
                #We need to undo the delimiting we put in place previously..
                ec = value.replace(cls.MSG_SPACE_SUB, ' ')
            elif key == cls.TC_TOKEN:
                tc = value
            elif key == cls.RC_TOKEN:
                rc = value 
            elif key == cls.RE_TOKEN:
                re = value
            elif key == cls.PE_TOKEN:
                pe = value
           
        
        return cls(ev, nm, en, ec, tc, rc, re, pe)      

    @staticmethod
    def toJSON(message):
        print 'GETTING JSON'
        msg = EventMessage.fromString(message)
        return json.dumps([ {'EV' : msg.event_type,
                            'NM' : msg.client_name,
                            'EN' : msg.event_name,
                            'EC' : msg.event_content,
                            'TC' : msg.event_destination,
                            'RC' : msg.need_client,
                            'RE' : msg.need_event,
                            'PE' : msg.provide_event }])

    def toString(self):
        retval = self.MSG_TOKEN
        
        if self.event_type is not None:
            retval += self.MSG_DELIM + self.EV_TOKEN + self.PAIR_SEPARATOR + self.event_type
        if self.client_name is not None:
            retval += self.MSG_DELIM + self.NM_TOKEN + self.PAIR_SEPARATOR + self.client_name
        if self.event_name is not None:
            retval += self.MSG_DELIM + self.EN_TOKEN + self.PAIR_SEPARATOR + self.event_name
        if self.event_content is not None:
            retval += self.MSG_DELIM + self.EC_TOKEN + self.PAIR_SEPARATOR + self.event_content
        if self.event_destination is not None:
            retval += self.MSG_DELIM + self.TC_TOKEN + self.PAIR_SEPARATOR + self.event_destination
        if self.need_client is not None:
            retval += self.MSG_DELIM + self.RC_TOKEN + self.PAIR_SEPARATOR + self.need_client
        if self.need_event is not None:
            retval += self.MSG_DELIM + self.RE_TOKEN + self.PAIR_SEPARATOR + self.need_event
        if self.provide_event is not None:
            retval += self.MSG_DELIM + self.PE_TOKEN + self.PAIR_SEPARATOR + self.provide_event
        
        logging.info('Message converted to string: ' + retval)
        
        return retval
        
        
class EventMessageBuilder(object):
    '''
    Conveinience class to help build valid event messages
    
    TODO: Add some validation to build()
    '''
    def __init__(self):
        self.event_type = None
        self.client_name = None
        self.event_name = None
        self.event_content = None
        self.event_destination = None
        self.need_client = None
        self.need_event = None
        self.provide_event = None
    
    def build(self):
        return EventMessage(self.event_type,
                            self.client_name,
                            self.event_name,
                            self.event_content,
                            self.event_destination,
                            self.need_client,
                            self.need_event,
                            self.provide_event)