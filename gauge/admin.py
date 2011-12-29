from django.contrib import admin

from gauge.models import BenchmarkResult, BenchmarkSuite, Branch, Repository, PythonVersion


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', )


class BenchmarkResultAdmin(admin.ModelAdmin):
    list_display = ('benchmark', 'suite', 'significant', 'delta_std', 'run_date',)
    list_filter = ('significant', 'suite', 'benchmark',)


class BenchmarkSuiteAdmin(admin.ModelAdmin):
    list_display = ('control', 'experiment', )


admin.site.register(Branch, BranchAdmin)
admin.site.register(BenchmarkResult, BenchmarkResultAdmin)
admin.site.register(BenchmarkSuite, BenchmarkSuiteAdmin)
admin.site.register(Repository)
admin.site.register(PythonVersion)
