from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('',
    #http://127.0.0.1/swarmingHeads/
    #    By default for now, show the login page as a home page
    #    In future, we should determine if user is already logged in
    #    and redirect accordingly
    url(r'^$', 'apps.swarmingHeads.views.login_page'),
    
    #The login page
    url(r'^login$', 'apps.swarmingHeads.views.login_page'),
    
    #http://127.0.0.1/swarmingHeads/login/handler
    #    Address used to validate login attempts
    url(r'^login/handler', 'apps.swarmingHeads.views.login_handler'),
)
