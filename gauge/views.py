from __future__ import absolute_import
import datetime

from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from django.forms.models import model_to_dict

from .models import Branch, Benchmark, BenchmarkSuite, BenchmarkResult


@cache_page(60 * 60)
def index(request):

    suites = BenchmarkSuite.objects.all()

    reports = []

    for suite in suites:
        for benchmark in Benchmark.objects.distinct().filter(benchmarkresult__suite=suite):
            reports.append({
                'suite': suite,
                'benchmark': benchmark,
            })

    return render(request, 'gauge/index.html', {
        'reports': reports,
    })


@cache_page(60 * 60)
def metric_detail(request, suite_id, metric_slug):
    suite = get_object_or_404(BenchmarkSuite, id=suite_id)
    benchmark = get_object_or_404(Benchmark, name=metric_slug)

    return render(request, 'gauge/detail.html', {
        'suite': suite,
        'benchmark': benchmark,
    })


@cache_page(60 * 60)
def metric_json(request, suite_id, metric_slug):
    suite = get_object_or_404(BenchmarkSuite, id=suite_id)

    try:
        benchmark = Benchmark.objects.get(name=metric_slug)
    except BenchmarkResult.DoesNotExist:
        raise http.Http404()

    try:
        daysback = int(request.GET['days'])
    except (TypeError, KeyError):
        daysback = 30

    d = datetime.datetime.now() - datetime.timedelta(days=daysback)

    doc = model_to_dict(benchmark)
    doc['data'] = benchmark.gather_data(since=d, suite=suite)

    return http.HttpResponse(
        simplejson.dumps(doc, indent=4 if settings.DEBUG else None),
        content_type="application/json",
    )
