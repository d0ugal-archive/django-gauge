from __future__ import absolute_import
import datetime

from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from django.forms.models import model_to_dict

from .models import Benchmark, BenchmarkSuite, BenchmarkResult


@cache_page(60 * 60)
def index(request, suite_ids=None):

    significant = 'significant' in request.GET

    if not suite_ids:
        suites = BenchmarkSuite.objects.distinct().filter(
                                    is_active=True, show_on_dashboard=True)
    else:
        suite_ids = suite_ids.split('+')
        suites = BenchmarkSuite.objects.filter(pk__in=suite_ids)

    return render(request, 'gauge/index.html', {
        'suites': suites,
        'significant': significant,
    })


@cache_page(60 * 60)
def metric_detail(request, suite_ids, metric_slug):

    significant = 'significant' in request.GET

    suite_ids_list = suite_ids.split('+')
    suites = BenchmarkSuite.objects.filter(pk__in=suite_ids_list)
    benchmark = get_object_or_404(Benchmark, name=metric_slug)

    return render(request, 'gauge/detail.html', {
        'suites': suites,
        'benchmark': benchmark,
        'significant': significant,
        'suite_ids': suite_ids,
        'versus': len(suites) > 1,
        'suite': suites[0],
    })


@cache_page(60 * 60)
def metric_json(request, suite_ids, metric_slug=None):

    significant = 'significant' in request.GET
    detail = 'detail' in request.GET

    suite_ids_list = suite_ids.split('+')
    suites = BenchmarkSuite.objects.filter(pk__in=suite_ids_list)

    if metric_slug:
        try:
            benchmarks = [Benchmark.objects.get(name=metric_slug)]
        except BenchmarkResult.DoesNotExist:
            raise http.Http404()
    else:
        benchmarks = Benchmark.objects.distinct().filter(benchmarksuite__pk__in=suite_ids_list)
        if significant:
            benchmarks = benchmarks.filter(benchmarkresult__significant=True)

    try:
        daysback = int(request.GET['days'])
    except (TypeError, KeyError):
        daysback = 30

    d = datetime.datetime.now() - datetime.timedelta(days=daysback)

    docs = []
    for benchmark in benchmarks:
        doc = model_to_dict(benchmark)
        doc['data'] = benchmark.gather_data(since=d, suites=suites,
            significant_only=significant, detail=detail)
        docs.append(doc)

    # HACK: If we have a metric slug, we only want to return one. Not all.
    if metric_slug:
        assert len(docs) == 1, len(docs)
        docs = docs[0]

    return http.HttpResponse(
        simplejson.dumps(docs, indent=4 if settings.DEBUG else None),
        content_type="application/json",
    )
