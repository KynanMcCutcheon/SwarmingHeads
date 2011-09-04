'''
Created on Aug 27, 2011

@author: Daniel Grech 16438385

@summary: 
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads import EM_INTERFACE
from swarming_heads.apps.testing.CometComponents import Comet
from swarming_heads.eminterface.EventMessage import EventMessage, \
    EventMessageBuilder
from swarming_heads.eminterface.Events import EventType, EventList
from swarming_heads.settings import STOMP_HOST, STOMP_PORT, ORBITED_HOST, \
    ORBITED_PORT
import logging

def em_test(request):
    #We are viewing the em page.. make sure we are connected
    #Note.. we may want to do this in a bg thread and show the user
    #some kind of dialog
    if not EM_INTERFACE.is_connected:
        success, err_msg = EM_INTERFACE.connect()
        if not success:
            Comet.push_message('Error connecting to event manager: ' + err_msg)
    
    template_file = 'testing/em_interface_test.html' 
    mappings = {'stomp_host' :   STOMP_HOST,
                'stomp_port' :   STOMP_PORT,
                'orbited_host' : ORBITED_HOST,
                'orbited_port' : ORBITED_PORT,
                'server_host' :  request.get_host()}
    return render_to_response(template_file,mappings, context_instance=RequestContext(request))

def send_message(request):
    if request.GET.has_key('message'):
        message = request.GET['message']
    else:
        logging.warning('Couldnt find message value in GET request')


    builder = EventMessageBuilder()
    
    builder.event_type = EventType.EVENT
    builder.event_name = EventList.TEXT_MESSAGE
    builder.client_name = 'tux'
    builder.event_destination = 'client1'
    builder.event_content = EventMessage.MSG_ARG_DELIM + message + EventMessage.MSG_ARG_DELIM

    success, err_msg = EM_INTERFACE.send_raw_string(builder.build().toString())
    
    if not success:
        # Send error message to client!
        Comet.push_message('Error sending message: ' + err_msg)
    else:
        return HttpResponse("OK")