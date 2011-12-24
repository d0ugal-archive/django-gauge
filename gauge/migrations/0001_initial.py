# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Benchmark'
        db.create_table('gauge_benchmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('gauge', ['Benchmark'])

        # Adding model 'Branch'
        db.create_table('gauge_branch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('gauge', ['Branch'])

        # Adding model 'BenchmarkSuite'
        db.create_table('gauge_benchmarksuite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('control', self.gf('django.db.models.fields.related.ForeignKey')(related_name='control_set', to=orm['gauge.Branch'])),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='experiment_set', to=orm['gauge.Branch'])),
            ('benchmark_runs', self.gf('django.db.models.fields.PositiveIntegerField')(default=1000)),
        ))
        db.send_create_signal('gauge', ['BenchmarkSuite'])

        # Adding unique constraint on 'BenchmarkSuite', fields ['control', 'experiment']
        db.create_unique('gauge_benchmarksuite', ['control_id', 'experiment_id'])

        # Adding model 'BenchmarkResult'
        db.create_table('gauge_benchmarkresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('suite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gauge.BenchmarkSuite'])),
            ('benchmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gauge.Benchmark'])),
            ('significant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('run_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('delta_avg', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('delta_min', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('delta_std', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avg_base', self.gf('django.db.models.fields.FloatField')()),
            ('avg_changed', self.gf('django.db.models.fields.FloatField')()),
            ('min_base', self.gf('django.db.models.fields.FloatField')()),
            ('min_changed', self.gf('django.db.models.fields.FloatField')()),
            ('std_base', self.gf('django.db.models.fields.FloatField')()),
            ('std_changed', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('gauge', ['BenchmarkResult'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BenchmarkSuite', fields ['control', 'experiment']
        db.delete_unique('gauge_benchmarksuite', ['control_id', 'experiment_id'])

        # Deleting model 'Benchmark'
        db.delete_table('gauge_benchmark')

        # Deleting model 'Branch'
        db.delete_table('gauge_branch')

        # Deleting model 'BenchmarkSuite'
        db.delete_table('gauge_benchmarksuite')

        # Deleting model 'BenchmarkResult'
        db.delete_table('gauge_benchmarkresult')


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
            'run_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'significant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'std_base': ('django.db.models.fields.FloatField', [], {}),
            'std_changed': ('django.db.models.fields.FloatField', [], {}),
            'suite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gauge.BenchmarkSuite']"})
        },
        'gauge.benchmarksuite': {
            'Meta': {'unique_together': "(['control', 'experiment'],)", 'object_name': 'BenchmarkSuite'},
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
