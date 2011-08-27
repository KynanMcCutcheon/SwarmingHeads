'''
Created on Aug 27, 2011

@author: daniel
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

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