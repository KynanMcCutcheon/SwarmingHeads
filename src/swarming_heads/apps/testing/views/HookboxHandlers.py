from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
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
def publish(request):
    #For now, this view simple echos back what it received
    
    print request.POST["action"]
    print request.POST["channel_name"]
    print request.POST["payload"]
        
    '''
    values = { "channel_name" : "/chat/",
               "payload" : []
             }
    
    url = "http://127.0.0.1:8001/rest/publish"
    
    values["payload"] = {"key1" : "val1",
                         "key2" : "val2"}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)
    '''
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)

@csrf_exempt
def disconnect(request):
    
    print 'DISCONNECTING BRO'
    jsonString = json.dumps([ True, {} ])
    
    return HttpResponse(content=jsonString, status=200)

def push_message(message):
    values = { "channel_name" : "/chat/",
               "payload" : message
             }
    
    url = "http://127.0.0.1:8001/rest/publish"
    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)

@csrf_exempt
def home(request):
    print 'GETTING HOME BRO'
    return render(request, 'testing/HookboxTest.html')