from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('gauge.views',
    url(r'^$', 'index', name="gauge-index"),
    url(r'^metric/(?P<control>[\w\-\.]+)/(?P<experiment>[\w\-\.]+)/(?P<metric_slug>[\w-]+)/$', 'metric_detail', name="benchmark-detail"),
    url(r'^metric/(?P<control>[\w\-\.]+)/(?P<experiment>[\w\-\.]+)/(?P<metric_slug>[\w-]+).json$', 'metric_json', name="benchmark-json"),
)
