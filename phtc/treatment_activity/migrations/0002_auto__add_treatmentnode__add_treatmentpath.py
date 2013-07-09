# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TreatmentNode'
        db.create_table('treatment_activity_treatmentnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('help', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('treatment_activity', ['TreatmentNode'])

        # Adding model 'TreatmentPath'
        db.create_table('treatment_activity_treatmentpath', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('tree', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['treatment_activity.TreatmentNode'])),
            ('cirrhosis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('treatment_status', self.gf('django.db.models.fields.IntegerField')()),
            ('drug_choice', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('treatment_activity', ['TreatmentPath'])


    def backwards(self, orm):
        # Deleting model 'TreatmentNode'
        db.delete_table('treatment_activity_treatmentnode')

        # Deleting model 'TreatmentPath'
        db.delete_table('treatment_activity_treatmentpath')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'css_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'treatment_activity.treatmentactivityblock': {
            'Meta': {'object_name': 'TreatmentActivityBlock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'treatment_activity.treatmentnode': {
            'Meta': {'object_name': 'TreatmentNode'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'help': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'treatment_activity.treatmentpath': {
            'Meta': {'object_name': 'TreatmentPath'},
            'cirrhosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'drug_choice': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'treatment_status': ('django.db.models.fields.IntegerField', [], {}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['treatment_activity.TreatmentNode']"})
        }
    }

    complete_apps = ['treatment_activity']