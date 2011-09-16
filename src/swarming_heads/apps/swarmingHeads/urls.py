from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('apps.swarmingHeads.views',
    url(r'^interface/$', 'interface'),
    
    url(r'^$', 'login_page'),
    
    #Handler for login attempts
    url(r'^login', 'login_handler'),
    
    #Receiver for comet messages
    url(r'^message/send/$', 'send_message'),
)
