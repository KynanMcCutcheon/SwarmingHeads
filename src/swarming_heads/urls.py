from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template

admin.autodiscover()

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('',
    # Pulls urls from the 'testing' app 
    (r'^test/', include('apps.testing.urls')),
    
    # Urls for our static files..
    url(r'^static/(?P<path>.*)', 'django.views.static.serve'),
    
    # Urls to handle admin work
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #Url to catch the homepage
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    
    #Most other pages are in the swarming heads app
    url(r'^swarmingHeads/', include('apps.swarmingHeads.urls')),
    
    
    #============================================================================
    #NOTE: From here down are page redirects
    #    E.g. the first one allows users to browse to http://127.0.0.1:8000/login
    #         and be redirected to http://127.0.0.1:8000/swarminHeads/login
    (r'^login$', redirect_to, {'url': 'swarmingHeads/login'}),
)
