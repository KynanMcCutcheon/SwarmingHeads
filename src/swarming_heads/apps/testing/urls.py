from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('',
    url(r'^$', 'apps.testing.views.index'),
    
    # E.g http://127.0.0.1:8000/test/12
    url(r'^(?P<user_id>\d+)/$', 'apps.testing.views.user_details'),

    #E.g. http://127.0.0.1:8000/test/template_test
    url(r'^template_test$', 'apps.testing.views.template_test'),
    
    #E.g. http://127.0.0.1:8000/test/form_test/12
    url(r'^form_test/(?P<user_id>\d+)/$', 'apps.testing.views.form_test'),
    
    #this url handles a submit of the form_test.
    url(r'^form_test/(?P<user_id>\d+)/set_username/$', 'apps.testing.views.set_username'),
    
    #An example showing off AJAX & comet capabilities
    url(r'^dynamic_test/(?P<user_id>\d+)/$', 'apps.testing.views.dynamic_test'),
    
    #this url handles the AJAX submit of the dynamic_test.
    url(r'^dynamic_test/(?P<user_id>\d+)/set_username/$', 'apps.testing.views.set_username'),
    
    url(r'^comet_test/$', 'apps.testing.views.comet_test'),
    
    #For the comet example
    url(r'^comet_test/xhr/$', 'apps.testing.views.xhr'),
)
