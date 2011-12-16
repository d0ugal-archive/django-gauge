from calendar import timegm
from datetime import datetime
from django.db import models


class Benchmark(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class BenchmarkSuite(models.Model):
    control = models.ForeignKey(Branch, related_name="control_set")
    experiment = models.ForeignKey(Branch, related_name="experiment_set")
    benchmarks = models.ManyToManyField(Benchmark, through='gauge.BenchmarkResult')

    class Meta:
        unique_together = ['control', 'experiment', ]

    def __unicode__(self):
        return "%s -> %s" % (self.control, self.experiment)


class BenchmarkResult(models.Model):
    suite = models.ForeignKey(BenchmarkSuite)
    benchmark = models.ForeignKey(Benchmark)

    significant = models.BooleanField(default=False)
    run_date = models.DateTimeField(default=datetime.now)

    delta_avg = models.CharField(max_length=100)
    delta_min = models.CharField(max_length=100)
    delta_std = models.CharField(max_length=100)
    avg_base = models.FloatField()
    avg_changed = models.FloatField()
    min_base = models.FloatField()
    min_changed = models.FloatField()
    std_base = models.FloatField()
    std_changed = models.FloatField()

    class Meta:
        ordering = ['benchmark__name', 'run_date', ]
        get_latest_by = 'run_date'

    def __unicode__(self):
        return "%s (%s vs %s)" % (self.benchmark, self.suite.control,
            self.suite.experiment)

    def gather_data(self, since):
        """
        Gather data from an "instant" metric.

        Instant metrics change every time we measure them, so they're easy:
        just return every single measurement.
        """
        data = BenchmarkResult.objects.filter(suite=self.suite,
            benchmark=self.benchmark, run_date__gt=since).order_by('run_date'
            ).values_list('run_date', 'avg_base', 'avg_changed')

        data_sets = []
        data_sets.append({'data': [(timegm(t.timetuple()), std)
            for (t, std, __) in data]})
        data_sets.append({'data': [(timegm(t.timetuple()), std)
            for (t, __, std) in data]})
        return data_sets
