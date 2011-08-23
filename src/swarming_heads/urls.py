from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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
)
