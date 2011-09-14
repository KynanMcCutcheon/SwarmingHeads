'''
Created on Sep 9, 2011

@author: daniel
'''
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def login_page(request):
    # Login page goes here!
    
    template_file = 'swarmingHeads/login.html'
    mappings = {}

    return render_to_response(template_file, mappings, 
                              context_instance=RequestContext(request))
    
    
def login_handler(request):    
    # KYNAN/DOM: ADD ERROR HANDLING!
    # If it cant find 'username' below, bad things happen
    # E.g. go to http://127.0.0.1:8000/swarmingHeads/login/handler
    # directly and watch it crash and burn :)
    #
    # Add and exception handler around the bottom 2 lines
    #    IF (HasException)
    #        Redirect to error page/login page
    #    ELSE
    #        Continue as normal
    
    username = request.POST['username']
    password = request.POST['password']
    
    print username, password
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # If isAdmin
            #    Go to some 'admin' page
            # Else if isUser
            #    Go to 'main' page
            return HttpResponse("LOGIN SUCCESSFUL, Thanks " + user.username)
            
        else:
            # Show a message to user saying to contact administrator
            return HttpResponse("ACCOUNT DISABLED")
    else:
        # Show error message on the page
        return HttpResponse("INVALID LOGIN")