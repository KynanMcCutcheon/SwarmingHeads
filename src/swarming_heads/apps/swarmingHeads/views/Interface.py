'''
Created on Sep 16, 2011
'''
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads.apps.hb.views import send_message
from swarming_heads.settings import HOOKBOX_PORT, HOOKBOX_HOST

def interface(request):
    if request.user.is_authenticated():
        #Valid user, lets show them the interface
        mappings = {'server_host'  : request.get_host(),
                    'hookbox_port' : HOOKBOX_PORT,
                    'hookbox_host' : HOOKBOX_HOST }
        return render_to_response('swarmingHeads/ui_index.html',mappings,context_instance=RequestContext(request))
    else:
        #User is not logged in, redirect them to login page
        return HttpResponseRedirect('/')
    
def pass_message(request):
    send_message(request)