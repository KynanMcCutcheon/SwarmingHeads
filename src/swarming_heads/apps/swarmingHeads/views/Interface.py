'''
Created on Sep 16, 2011
'''
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads.settings import STOMP_HOST, STOMP_PORT, ORBITED_HOST, \
    ORBITED_PORT
def interface(request):
    if request.user.is_authenticated():
        #Valid user, lets show them the interface
        mappings = {'stomp_host' : STOMP_HOST, 
                    'stomp_port' : STOMP_PORT, 
                    'orbited_host' : ORBITED_HOST, 
                    'orbited_port' : ORBITED_PORT, 
                    'server_host' :  request.get_host()}
        return render_to_response('swarmingHeads/ui_index.html',mappings,context_instance=RequestContext(request))
    else:
        #User is not logged in, redirect them to login page
        return HttpResponseRedirect('/')