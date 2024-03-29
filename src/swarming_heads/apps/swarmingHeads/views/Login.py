'''
Created on Sep 9, 2011
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads.apps.swarmingHeads.forms import LoginForm
        
def login_page(request):
    if request.user.is_authenticated():
        #We're already logged in, lets go straight to the index
        return HttpResponseRedirect('/interface/')
    else:
        #Not logged in, render to login screen
        mappings = {'form': LoginForm(),}
        
        if request.session.has_key('login_error'):
            #If we have an error to display, lets get it
            mappings['login_error'] =  request.session['login_error']

        #PAT!!!
        #    On the login page, you can put a template tag {{ login_error }}
        #    which can indicate there was an error on the previous login attempt

        return render_to_response('swarmingHeads/ui_login.html', mappings, context_instance=RequestContext(request))
    
def login_handler(request):       
    if request.method == "POST":    
        loginform = LoginForm(request.POST)
        if loginform.login(request):            
            return HttpResponseRedirect('/interface/')
        
    #User is not logged in, redirect them to login page
    #NOTE: Somehow need to indicate we need to show an error message on the page
    #      E.g. ?error="CouldntLogIn"
    request.session['login_error'] = 'Error logging in'
    return HttpResponseRedirect('/')
 