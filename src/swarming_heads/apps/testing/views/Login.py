'''
Created on Sep 9, 2011

@author: daniel
'''
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def login_test(request):
    # Login page goes here!
    
    template_file = 'testing/login_test.html'
    mappings = {}

    return render_to_response(template_file, mappings, 
                              context_instance=RequestContext(request))
    
    
def login_handler(request):    
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
            return HttpResponse("LOGIN SUCCESSFUL")
            
        else:
            # Show a message to user saying to contact administrator
            return HttpResponse("ACCOUNT DISABLED")
    else:
        # Show error message on the page
        return HttpResponse("INVALID LOGIN")