'''
Created on Sep 9, 2011

@author: daniel
'''
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads.apps.swarmingHeads.forms import LoginForm
from swarming_heads.settings import STOMP_HOST, STOMP_PORT, ORBITED_HOST, \
    ORBITED_PORT

def login_page(request):
    form = LoginForm()
    return render_to_response('swarmingHeads/ui_login.html',{'form': form,},context_instance=RequestContext(request))
    
def login_handler(request):       
    if request.method == "POST":    
        loginform = LoginForm(request.POST)
        if loginform.login(request):            
            mappings = {'stomp_host' : STOMP_HOST, 'stomp_port' : STOMP_PORT, 'orbited_host' : ORBITED_HOST, 'orbited_port' : ORBITED_PORT, 'server_host' :  request.get_host()}
            return render_to_response('swarmingHeads/ui_index.html',mappings,context_instance=RequestContext(request))
        
    loginform = LoginForm()
    return HttpResponse("INVALID LOGIN")
 