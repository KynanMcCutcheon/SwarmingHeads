from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template

admin.autodiscover()

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('',    
    # Urls for our static files..
    url(r'^static/(?P<path>.*)', 'django.views.static.serve'),
    
    # Urls to handle admin work
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #All other urls are handled in the swarmingHeads app
    url(r'^',  include('apps.swarmingHeads.urls')),
)
