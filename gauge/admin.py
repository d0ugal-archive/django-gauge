from django.contrib import admin

from gauge.models import BenchmarkResult, BenchmarkSuite, Branch, Repository, PythonVersion


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BenchmarkResultAdmin(admin.ModelAdmin):
    list_display = ('benchmark', 'suite', 'significant', 'delta_std', 'run_date',)
    list_filter = ('significant', 'suite', 'benchmark',)

    def queryset(self, request):
        qs = super(BenchmarkResultAdmin, self).queryset(request)
        return qs.defer("raw")


class BenchmarkSuiteAdmin(admin.ModelAdmin):
    list_display = ('python_version', 'repository', 'control', 'experiment',
        'benchmark_runs', 'is_active', 'show_on_dashboard', 'results')
    list_editable = ('is_active', 'show_on_dashboard',)
    save_as = True

    def results(self, obj):
        return BenchmarkResult.objects.filter(suite=obj.id).count()


admin.site.register(Branch, BranchAdmin)
admin.site.register(BenchmarkResult, BenchmarkResultAdmin)
admin.site.register(BenchmarkSuite, BenchmarkSuiteAdmin)
admin.site.register(Repository)
admin.site.register(PythonVersion)
