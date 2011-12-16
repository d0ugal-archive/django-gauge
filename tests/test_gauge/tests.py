from django.test import TestCase


class TestBenchmarkRun(TestCase):

    def test_run(self):

        from gauge.tasks import run_benchmarks
        from gauge.models import BenchmarkSuite, Branch

        b13 = Branch.objects.create(name="1.3")
        bmaster = Branch.objects.create(name="master")
        BenchmarkSuite.objects.create(control=b13, experiment=bmaster)

        run_benchmarks()
