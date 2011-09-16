from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('apps.swarmingHeads.views',
    #Need to put an index page here!
    url(r'^$', 'index'),
    
    #The login page
    url(r'^login$', 'login_page'),
    
    #Receiver for comet messages
    url(r'^message/send/$', 'send_message'),
    
    #http://127.0.0.1/swarmingHeads/login/handler
    #    Address used to validate login attempts
    url(r'^login/handler', 'login_handler'),
)
