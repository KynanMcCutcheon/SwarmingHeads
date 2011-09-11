'''
Created on Aug 27, 2011

@author: daniel
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads.eminterface.CometComponents import Comet
from swarming_heads.settings import STOMP_HOST, STOMP_PORT, ORBITED_HOST, \
    ORBITED_PORT
import logging

def comet_test(request):
    template_file = 'testing/comet_test.html' 
    
    mappings = {'stomp_host' :   STOMP_HOST,
                'stomp_port' :   STOMP_PORT,
                'orbited_host' : ORBITED_HOST,
                'orbited_port' : ORBITED_PORT,
                'server_host' :  request.get_host()}
    return render_to_response(template_file,mappings, context_instance=RequestContext(request))  
    
def xhr(request):
    # see what message has been sent
    if request.GET.has_key('message'):
        message = request.GET['message']
    else:
        logging.warning('Couldnt find message value in GET request')

    # push the data to all clients.
    Comet.push_message(message)

    # That's it, thread's not locked
    return HttpResponse("OK")