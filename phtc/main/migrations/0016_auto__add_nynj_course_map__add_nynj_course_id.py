# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NYNJ_Course_Map'
        db.create_table('main_nynj_course_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course_map', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.NYNJ_Course_ID'], unique=True)),
            ('phtc_url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['NYNJ_Course_Map'])

        # Adding model 'NYNJ_Course_ID'
        db.create_table('main_nynj_course_id', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseID', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['NYNJ_Course_ID'])


    def backwards(self, orm):
        # Deleting model 'NYNJ_Course_Map'
        db.delete_table('main_nynj_course_map')

        # Deleting model 'NYNJ_Course_ID'
        db.delete_table('main_nynj_course_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.dashboardinfo': {
            'Meta': {'object_name': 'DashboardInfo'},
            'dashboard': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pagetree.Section']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {})
        },
        'main.nynj_course_id': {
            'Meta': {'object_name': 'NYNJ_Course_ID'},
            'courseID': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.nynj_course_map': {
            'Meta': {'object_name': 'NYNJ_Course_Map'},
            'course_map': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.NYNJ_Course_ID']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phtc_url': ('django.db.models.fields.TextField', [], {})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age': ('django.db.models.fields.TextField', [], {}),
            'degree': ('django.db.models.fields.TextField', [], {}),
            'dept_health': ('django.db.models.fields.TextField', [], {}),
            'disadvantaged': ('django.db.models.fields.TextField', [], {}),
            'employment_location': ('django.db.models.fields.TextField', [], {}),
            'ethnicity': ('django.db.models.fields.TextField', [], {}),
            'experience': ('django.db.models.fields.TextField', [], {}),
            'fname': ('django.db.models.fields.TextField', [], {}),
            'geo_dept_health': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.TextField', [], {}),
            'origin': ('django.db.models.fields.TextField', [], {}),
            'other_employment_location': ('django.db.models.fields.TextField', [], {}),
            'other_position_category': ('django.db.models.fields.TextField', [], {}),
            'position': ('django.db.models.fields.TextField', [], {}),
            'rural': ('django.db.models.fields.TextField', [], {}),
            'sex': ('django.db.models.fields.TextField', [], {}),
            'umc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'work_city': ('django.db.models.fields.TextField', [], {}),
            'work_state': ('django.db.models.fields.TextField', [], {}),
            'work_zip': ('django.db.models.fields.TextField', [], {})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
        }
    }

    complete_apps = ['main']