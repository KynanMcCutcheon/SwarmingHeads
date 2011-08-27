'''
Created on Aug 27, 2011

@author: daniel
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def set_username(request, user_id):
    #This view is called via ajax!
    
    #Get the username
    if request.GET.has_key('user_name'):
        return HttpResponse("The server says that user " + user_id +" has had his name set to '" + request.GET['user_name'] + "'")
    else:
        return HttpResponse("The server says sorry user " + user_id + ", could find a username")

def dynamic_test(request, user_id):
    # This will be the same as the 'form_test', except it will use AJAX to
    # get a response. The templates used are exactly the same, except in 
    # dynamic_test.html, we have added the '?xhr' argument to the submission call
    # We can use this to differentiate when the page is requested via AJAX,
    # or by a normal POST submission
    template_file = 'testing/dynamic_test.html'
    mappings = {'user_id' : user_id}
        
    return render_to_response(template_file, mappings, 
                              context_instance=RequestContext(request))