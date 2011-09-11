from django.conf.urls.defaults import patterns, url

# See https://docs.djangoproject.com/en/dev/intro/tutorial03/#design-your-urls
# to understand what is going on here
urlpatterns = patterns('',
    url(r'^$', 'apps.swarmingHeads.views.login'),
)
