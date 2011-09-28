from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('apps.swarmingHeads.views',
    url(r'^interface/$', 'interface'),
    
    url(r'^$', 'login_page'),
    
    #Handler for login attempts
    url(r'^login', 'login_handler'),
    
    #Handler for logout attempt
    url(r'^interface/logout', 'logout_handler'),
        
    #Hookbox callbacks
    (r'^connect$', 'connect'),
    (r'^create_channel$', 'create_channel'),
    (r'^subscribe', 'subscribe'),
    (r'^disconnect', 'disconnect'),
    (r'^publish', 'publish'),
)
