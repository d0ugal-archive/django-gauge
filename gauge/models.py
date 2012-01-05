from calendar import timegm
from datetime import datetime
from django.db import models

VCS_CHOICES = (
    ('git', 'git'),
    ('hg', 'hg'),
)


class PythonVersion(models.Model):
    name = models.CharField(max_length=15)
    binary = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.binary)


class Repository(models.Model):
    vcs_type = models.CharField(max_length=5, choices=VCS_CHOICES)
    url = models.CharField(max_length=300)

    def __unicode__(self):
        return "%s - %s" % (self.vcs_type, self.url)


class Benchmark(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def gather_data(self, since, suites, significant_only, detail=False):
        """
        Gather data from an "instant" metric.

        Instant metrics change every time we measure them, so they're easy:
        just return every single measurement.
        """

        data_sets = []

        multi = len(suites) > 1

        for suite in suites:

            data = BenchmarkResult.objects.filter(suite=suite,
                benchmark=self, run_date__gt=since).order_by('run_date')

            if significant_only:
                data = data.filter(significant=True)

            if not detail:

                fields = ['run_date', 'avg_base', 'avg_changed']

            else:

                fields = ['run_date', 'avg_base', 'avg_changed',
                    'min_base', 'min_changed']

            data = data.values_list(*fields)

            for i, field in enumerate(fields):

                if field == 'run_date':
                    continue

                data_values = []

                for values in data:
                    data_values.append((timegm(values[0].timetuple()), values[i]))

                if multi:
                    field_label = "%s (%s)" % (field, suite.description)
                else:
                    field_label = field

                data_sets.append({
                    'label': field_label,
                    'data': data_values,
                })

        return data_sets


class Branch(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class BenchmarkSuite(models.Model):
    description = models.TextField(default="")
    python_version = models.ForeignKey(PythonVersion)
    repository = models.ForeignKey(Repository)
    control = models.ForeignKey(Branch, related_name="control_set")
    experiment = models.ForeignKey(Branch, related_name="experiment_set")
    benchmarks = models.ManyToManyField(Benchmark, through='gauge.BenchmarkResult')
    benchmark_runs = models.PositiveIntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    show_on_dashboard = models.BooleanField(default=True)

    class Meta:
        ordering = ['id', ]
        unique_together = ['python_version', 'repository', 'control', 'experiment', 'benchmark_runs']

    def significant_benchmarks(self):
        return self.benchmarks.distinct().filter(benchmarkresult__significant=True)

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

    raw = models.TextField()

    class Meta:
        ordering = ['benchmark__name', 'run_date', ]
        get_latest_by = 'run_date'

    def __unicode__(self):
        return "%s (%s vs %s)" % (self.benchmark, self.suite.control,
            self.suite.experiment)
