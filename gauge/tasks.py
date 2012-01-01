from json import loads
from os import listdir
from tempfile import mkdtemp

from celery import task
from django.core.cache import cache
from fabric.api import put, run, cd, get, env
from fabulaws.ec2 import SmallLucidInstance
from unipath import Path

from gauge import WORKER_BUNDLE
from gauge.models import BenchmarkResult, Benchmark, BenchmarkSuite, Repository


class OldSmallLucidInstance(SmallLucidInstance):
    run_upgrade = False


def _build_command(control, experiment, output, vcs, runs=1000):
    return ['djangobench', '--vcs=%s' % vcs, '--control=%s' % control,
            '--trials=%s' % runs, '--experiment=%s' % experiment,
            '--record=%s' % output, '--continue-on-error']


def _get_temp_dir():
    temp_dir = mkdtemp()
    return Path(temp_dir).expand().absolute()


def process_output(suite, path):

    for i, benchmark_output in enumerate(listdir(path)):

        name = benchmark_output.split('.')[0]

        benchmark_result = path.child(benchmark_output)
        json_file = open(benchmark_result)
        json_string = json_file.read()
        benchmark_result = loads(json_string)

        result = benchmark_result['result']

        if 't_msg' not in result:
            continue

        is_significant = result['t_msg'].startswith("Significant")
        benchmark, created = Benchmark.objects.get_or_create(name=name)

        BenchmarkResult.objects.create(benchmark=benchmark, suite=suite,
            significant=is_significant, min_base=result['min_base'],
            min_changed=result['min_changed'], delta_min=result['delta_min'],
            avg_base=result['avg_base'], avg_changed=result['avg_changed'],
            delta_avg=result['delta_avg'], std_base=result['std_base'],
            std_changed=result['std_changed'], delta_std=result['delta_std'],
            raw=json_string)


@task.task()
def run_benchmarks():

    env.output_prefix = False

    with OldSmallLucidInstance(terminate=True):

        run('mkdir ~/gauge/')
        run('mkdir ~/gauge/output/')

        for f in ['bootstrap.sh', 'requirements.txt']:
            local_f = Path(WORKER_BUNDLE, f)
            put(local_f, '~/gauge/', mirror_local_mode=True)

        run('chmod +x ~/gauge/bootstrap.sh')
        run('~/gauge/bootstrap.sh')

        for repo in Repository.objects.filter(benchmarksuite__is_active=True).distinct():
            if repo.vcs_type == 'git':
                run('git clone %s ~/gauge/django_%s' % (repo.url, repo.id))
            elif repo.vcs_type == 'hg':
                run('hg clone %s ~/gauge/django_%s' % (repo.url, repo.id))

        for suite in BenchmarkSuite.objects.filter(is_active=True):

            record_dir = _get_temp_dir()

            run('rm -rf ~/gauge/output/*')

            with cd('~/gauge/django_%s' % suite.repository.id):
                command = ' '.join(_build_command(suite.control,
                    suite.experiment, '~/gauge/output/',
                    suite.repository.vcs_type, suite.benchmark_runs))
                print command
                run(command)

            get('~/gauge/output/', local_path=record_dir)

            process_output(suite, record_dir.child('output'))

    print "Done."

    cache.clear()
