from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from swarming_heads import EM_INTERFACE
from swarming_heads.apps.eminterface.EventMessage import EventMessage
from swarming_heads.apps.testing.Comet import Comet
from swarming_heads.settings import RPC_SERVER_HOST, RPC_SERVER_PORT, \
    ORBITED_HOST, ORBITED_PORT, STOMP_HOST, STOMP_PORT
import logging
import xmlrpclib

# Some sample views
# Each is a simple, valid python function
# You can put what ever you want in each of these functions
# (E.g. call the event manager library), all that django needs 
# is to be returned a HttpResponse.

def index(request):
    return HttpResponse('<p>This is a custom view response!</p>')

def user_details(request, user_id):
    response = '<p>This demonstrates how we can get url parts..</p>'
    response += '<p>For example, this page was called with an url part ' + user_id
    return HttpResponse(response)

def template_test(request):
    #The template file we want to fill in
    template_file = 'testing/template_test.html'
    
    # A map containing the name of the template tag, and the value
    # to substitute
    mappings = {'tag_1': 'This has been substituted for tag_1',
                'tag_2': 'This has been substituted for tag_2',
                'tag_3': 'This has been substituted for tag_3',
                'tag_4': 'This has been substituted for tag_4',
                'tag_5': 'This has been substituted for tag_5',
                'conditional' : True} 
    
    return render_to_response(template_file, mappings)

def form_test(request, user_id):
    template_file = 'testing/form_test.html'
    mappings = {'user_id' : user_id}

    # Last argument here is djangos way of taking care of Cross site scripting for
    # us. Basically, anywhere we have a form, we need to include the {% csrf_token %}
    # tag on the page, and set the associated context_instance flag
    return render_to_response(template_file, mappings, 
                              context_instance=RequestContext(request))

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
    