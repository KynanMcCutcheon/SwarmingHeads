from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.hb.views',
    (r'^connect$', 'connect'),
    (r'^create_channel$', 'create_channel'),
    (r'^subscribe', 'subscribe'),
    (r'^disconnect', 'disconnect'),
    (r'^publish', 'publish'),
)
