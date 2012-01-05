from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('gauge.views',
    url(r'^$', 'index', name="gauge-index"),
    url(r'^(?P<suite_ids>[\d\+]+)/$', 'index', name="gauge-index"),
    url(r'^metric/(?P<suite_ids>[\d\+]+)/(?P<metric_slug>[\w-]+)/$', 'metric_detail', name="benchmark-detail"),
    url(r'^metric/(?P<suite_ids>[\d\+]+).json$', 'metric_json', name="benchmark-json"),
    url(r'^metric/(?P<suite_ids>[\d\+]+)/(?P<metric_slug>[\w-]+).json$', 'metric_json', name="benchmark-json"),
)
