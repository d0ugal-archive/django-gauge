# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'BenchmarkResult.raw'
        db.add_column('gauge_benchmarkresult', 'raw', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'BenchmarkResult.raw'
        db.delete_column('gauge_benchmarkresult', 'raw')


    models = {
        'gauge.benchmark': {
            'Meta': {'ordering': "['name']", 'object_name': 'Benchmark'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'gauge.benchmarkresult': {
            'Meta': {'ordering': "['benchmark__name', 'run_date']", 'object_name': 'BenchmarkResult'},
            'avg_base': ('django.db.models.fields.FloatField', [], {}),
            'avg_changed': ('django.db.models.fields.FloatField', [], {}),
            'benchmark': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.Benchmark']"}),
            'delta_avg': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'delta_min': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'delta_std': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_base': ('django.db.models.fields.FloatField', [], {}),
            'min_changed': ('django.db.models.fields.FloatField', [], {}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'run_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'significant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'std_base': ('django.db.models.fields.FloatField', [], {}),
            'std_changed': ('django.db.models.fields.FloatField', [], {}),
            'suite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.BenchmarkSuite']"})
        },
        'gauge.benchmarksuite': {
            'Meta': {'unique_together': "(['control', 'experiment', 'benchmark_runs'],)", 'object_name': 'BenchmarkSuite'},
            'benchmark_runs': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1000'}),
            'benchmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gauge.Benchmark']", 'through': "orm['gauge.BenchmarkResult']", 'symmetrical': 'False'}),
            'control': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'control_set'", 'to': "orm['gauge.Branch']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiment_set'", 'to': "orm['gauge.Branch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'gauge.branch': {
            'Meta': {'object_name': 'Branch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['gauge']
