from __future__ import unicode_literals, print_function

from optparse import make_option

from django.core.management.base import NoArgsCommand

from gauge.tasks import run_benchmarks


class Command(NoArgsCommand):

    option_list = NoArgsCommand.option_list + (
        make_option('-I', '--inline', action="store_true", dest='inline', ),
    )

    help = "Refresh the git repo dir"

    def handle(self, inline, *args, **kwargs):

        if inline:
            run_benchmarks()
        else:
            run_benchmarks.delay()
