from django.contrib import admin

from gauge.models import BenchmarkResult, BenchmarkSuite, Branch, Repository, PythonVersion


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BenchmarkResultAdmin(admin.ModelAdmin):
    list_display = ('benchmark', 'suite', 'significant', 'delta_std', 'run_date',)
    list_filter = ('significant', 'suite', 'benchmark',)


class BenchmarkSuiteAdmin(admin.ModelAdmin):
    list_display = ('python_version', 'repository', 'control', 'experiment',
        'benchmark_runs', 'is_active', 'results')
    list_editable = ('is_active',)

    def results(self, obj):
        return BenchmarkResult.objects.filter(suite=obj.id).count()


admin.site.register(Branch, BranchAdmin)
admin.site.register(BenchmarkResult, BenchmarkResultAdmin)
admin.site.register(BenchmarkSuite, BenchmarkSuiteAdmin)
admin.site.register(Repository)
admin.site.register(PythonVersion)
