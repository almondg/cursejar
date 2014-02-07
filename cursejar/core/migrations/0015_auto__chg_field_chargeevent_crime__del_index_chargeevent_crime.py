# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'ChargeEvent.crime' to match new field type.
        db.rename_column(u'core_chargeevent', 'crime_id', 'crime')
        # Changing field 'ChargeEvent.crime'
        db.alter_column(u'core_chargeevent', 'crime', self.gf('django.db.models.fields.CharField')(max_length=128))
        # Removing index on 'ChargeEvent', fields ['crime']
        db.delete_index(u'core_chargeevent', ['crime_id'])


    def backwards(self, orm):
        # Adding index on 'ChargeEvent', fields ['crime']
        db.create_index(u'core_chargeevent', ['crime_id'])


        # Renaming column for 'ChargeEvent.crime' to match new field type.
        db.rename_column(u'core_chargeevent', 'crime', 'crime_id')
        # Changing field 'ChargeEvent.crime'
        db.alter_column(u'core_chargeevent', 'crime_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Word']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 14, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'participant': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'challenges'", 'symmetrical': 'False', 'to': u"orm['core.Person']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'word1': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'word2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'word3': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'core.chargeevent': {
            'Meta': {'object_name': 'ChargeEvent'},
            'crime': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'date_of_felony': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'evidence': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'felon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Jar']"})
        },
        u'core.jar': {
            'Meta': {'object_name': 'Jar'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Challenge']"}),
            'current_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'user_profile'"},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.word': {
            'Meta': {'unique_together': "(('name', 'challenge'),)", 'object_name': 'Word'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Challenge']"}),
            'fine': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['core']