** Work in progress **


Django gauge
========================================
Automatically runs and displays the results of djangobench over time. This
is the code behind http://dgauge.ep.io/ (which wraps the app in a simple )


How to run it
========================================

1. pip install with something like `pip install -e git://github.com/d0ugal/django-gauge.git#egg=gauge`
2. Add 'gauge' to your installed apps, syncdb and migrate
3. Add the urls: url(r'^', include('gauge.urls')),
4. Collect static
5. Set the enviroment variables; AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
6. Run ./manage.py gauge_run_benchmarks -I


Help wanted
========================================

Any tips or suggestions how to make the results easlier to consume would be
appreciated. It's working well, but I could do help with the stats work to
improve the results and presentation.


Thanks
========================================
Thanks to Jacob Kaplan-Moss for creating djangobench and django-dev-dashboard
(from which much code was borrowered).
