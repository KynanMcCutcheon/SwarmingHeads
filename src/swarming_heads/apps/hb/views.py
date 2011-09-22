from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from swarming_heads import EM_INTERFACE
from swarming_heads.eminterface.EventMessage import EventMessageBuilder, \
    EventMessage
from swarming_heads.eminterface.Events import EventType, EventList
from swarming_heads.eminterface.MessagePassing import send_message
import json
import logging
import urllib
import urllib2

@csrf_exempt
def connect(request):
    
    print 'CONNECTING BRO'
    jsonString = json.dumps([ True, { "name" : "daniel" } ])
    
    return HttpResponse(content=jsonString, status=200)
    
    
@csrf_exempt
def create_channel(request):
    
    print 'CREATING CHANNEL BRO'
    jsonString = json.dumps([ True, { "history_size" : 0, 
                                    "reflective" : True, 
                                    "presenceful" : True } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def subscribe(request):
    
    print 'SUBSCRIBING BRO'
    jsonString = json.dumps([ True, {  } ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def disconnect(request):
    
    print 'DISCONNECTING BRO'
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)


@csrf_exempt
def publish(request):
    return send_message(request)