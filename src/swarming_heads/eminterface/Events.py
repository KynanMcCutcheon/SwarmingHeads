'''
Created on Sep 4, 2011

'''

class EventType(object):
    '''
    Defines the list of possible values which can be put in the 'EV'
    field of each message
    '''
    NEW = 'NEW'
    DELETE = 'DEL'
    EVENT = 'EVENT'
    ERROR = 'ERROR'

class EventList(object):
    '''
    This class defines the list of events which will be sent.
    It is assumed that by sending these events the EventManager will
    instruct the given robot to follow out the appropriate action
    
    These are the only values which should be passed to the constructor
    of class 'Event'
    
    Comment next to each command specifies what will be passed in the 'EC'
    portion of the message. E.g.:
    
        TEXT_MESSAGE = 'TXT' #Argument: A string message to send
        
    denotes that a message will be sent with EN = 'TXT' and EC = '<some string>' 
    
    It is expected that all these messages will have EventType.EVENT in the
    'EV' field of the message
    '''
    
    # Commands for robot movement
    MOVE_LEFT = 'MV_L' #Argument: Distance to move
    MOVE_RIGHT = 'MV_R' #Argument: Distance to move
    MOVE_FORWARD = 'MV_F' #Argument: Distance to move
    MOVE_BACKWARD = 'MV_B' #Argument: Distance to move
    ROTATE_LEFT = 'RT_L' #Argument: Rotation amount in degrees
    ROTATE_RIGHT = 'RT_R' #Argument: Rotation amount in degrees
    
    TEXT_MESSAGE = 'TXT' #Argument: A string message to send
    
    # Toggles to change robot settings
    TOGGLE_AUTOMATIC_CHAT = 'AUTO_CHAT' #Argument: '1' to turn on automatic replying, 0 to turn off
    TOGGLE_AUTOMATIC_MOVEMENT = 'AUTO_MV' #Argument: '1' to turn on automatic movement, 0 to turn off

class ErrorList(object):
    '''
    Class which defines various errors which can be received FROM
    the event manager
    
    Where possible, the 'EC' field of each message will have some
    sort of verbose explanation of the error that occured.
    
    It is expected that all these messages will have EventType.ERROR in the
    'EV' field of the message
    '''
    
    ERROR_CANT_MOVE = 'E_MV' #Received a movement command it couldn't complete
    ERROR_CANT_ROTATE = 'E_RT' #Received a rotate command it couldn't complete
    ERROR_RECEIVED_CORRUPT_MSG = 'E_CM' #Received a message which couldn't even be parsed
    ERROR_CANT_TOGGLE_CHAT = 'E_TC' #Error turning on/off automatic chat
    ERROR_CANT_TOGGLE_MOVEMENT = 'E_TM'#Error turning on/off automatic movement
    
    ERROR_UNKNOWN = 'E_U' #A last 'catch-all' for when an unknown error occurs
    
class Event(object):
    '''
    Simple class to hold details about an event
    '''
    def __init__(self, evt_name, evt_arg):
        self.name = evt_name #Value to send in 'EN'
        self.arg = evt_arg #Value to send in 'EC'
        