'''
Created on Aug 27, 2011

@author: Daniel Grech 16438385

@summary: 
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads import EM_INTERFACE
from swarming_heads.eminterface.EventMessage import EventMessage
from swarming_heads.settings import STOMP_HOST, STOMP_PORT, ORBITED_HOST, \
    ORBITED_PORT
import logging
import sys

def em_test(request):
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
    
    success, err_msg = EM_INTERFACE.send_message(EventMessage.fromString('EV:EVENT EN:ANSWER_THIS NM:tux EC:*' + message + '* TC:client1'))
    
    if not success:
        # Send error message to client!
        pass
    else:
        return HttpResponse("OK")