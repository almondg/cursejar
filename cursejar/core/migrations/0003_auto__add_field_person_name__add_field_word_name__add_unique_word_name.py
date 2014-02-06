# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.name'
        db.add_column(u'core_person', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'Word.name'
        db.add_column(u'core_word', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding unique constraint on 'Word', fields ['name', 'challenge']
        db.create_unique(u'core_word', ['name', 'challenge_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Word', fields ['name', 'challenge']
        db.delete_unique(u'core_word', ['name', 'challenge_id'])

        # Deleting field 'Person.name'
        db.delete_column(u'core_person', 'name')

        # Deleting field 'Word.name'
        db.delete_column(u'core_word', 'name')


    models = {
        u'core.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.chargeevent': {
            'Meta': {'object_name': 'ChargeEvent'},
            'crime': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Word']"}),
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
            'challenges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'participants'", 'null': 'True', 'to': u"orm['core.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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