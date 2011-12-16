from tempfile import mkdtemp
from json import load

from celery import task
from django.conf import settings
from djangobench.main import discover_benchmarks, DEFAULT_BENCMARK_DIR
from unipath import Path
from fabric.api import put, run, cd, get
from fabulaws.ec2 import SmallLucidInstance

from gauge.models import BenchmarkResult, Benchmark, BenchmarkSuite


class OldSmallLucidInstance(SmallLucidInstance):
    run_upgrade = False


def _build_command(control, experiment, output):
    return ['djangobench', '--vcs=git', '--control=%s' % control,
            '--trials=100', '--experiment=%s' % experiment,
            '--record=%s' % output]


def _get_temp_dir():
    temp_dir = mkdtemp()
    return Path(temp_dir).expand().absolute()


def process_output(suite, path):

    for i, benchmark in enumerate(discover_benchmarks(DEFAULT_BENCMARK_DIR)):

        benchmark_result = path.child('%s.json' % benchmark.name)
        benchmark_result = load(open(benchmark_result))

        result = benchmark_result['result']

        if 't_msg' not in result:
            continue

        is_significant = result['t_msg'].startswith("Significant")
        benchmark, created = Benchmark.objects.get_or_create(name=benchmark.name)

        BenchmarkResult.objects.create(benchmark=benchmark, suite=suite,
            significant=is_significant, min_base=result['min_base'],
            min_changed=result['min_changed'], delta_min=result['delta_min'],
            avg_base=result['avg_base'], avg_changed=result['avg_changed'],
            delta_avg=result['delta_avg'], std_base=result['std_base'],
            std_changed=result['std_changed'], delta_std=result['delta_std'])


@task.task()
def run_benchmarks():

    results = []

    with OldSmallLucidInstance(terminate=True):

        run('mkdir ~/gauge/')
        run('mkdir ~/gauge/output/')

        for f in ['bootstrap.sh', 'requirements.txt']:
            local_f = Path(settings.WORKER_BUNDLE, f)
            put(local_f, '~/gauge/', mirror_local_mode=True)

        run('chmod +x ~/gauge/bootstrap.sh')
        run('~/gauge/bootstrap.sh')
        run('git clone https://github.com/django/django.git ~/gauge/django')

        for suite in BenchmarkSuite.objects.all():

            record_dir = _get_temp_dir()

            run('rm -rf ~/gauge/output/*')

            with cd('~/gauge/django'):
                command = ' '.join(_build_command(suite.control,
                    suite.experiment, '~/gauge/output/'))
                run(command)

            get('~/gauge/output/', local_path=record_dir)

            results.append((suite, record_dir.child('output')))

    for suite, path in results:
        process_output(suite, path)

    print "done."
