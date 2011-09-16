from django.http import HttpResponse
from swarming_heads import EM_INTERFACE
from swarming_heads.eminterface.CometComponents import Comet
from swarming_heads.eminterface.EventMessage import EventMessageBuilder, \
    EventMessage
from swarming_heads.eminterface.Events import EventType, EventList
import logging


def send_message(request):
    if not EM_INTERFACE.is_connected:
        success, err_msg = EM_INTERFACE.connect(request.user.username)
        if not success:
            Comet.push_message('Error connecting to event manager: ' + err_msg)
    
    if request.GET.has_key('message'):
        message = request.GET['message']
    else:
        logging.warning('Couldnt find message value in GET request')


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
        Comet.push_message('Error sending message: ' + err_msg)
    else:
        return HttpResponse("OK")