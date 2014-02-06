# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field challenges on 'Person'
        db.delete_table(db.shorten_name(u'core_person_challenges'))

        # Adding M2M table for field participants on 'Challenge'
        m2m_table_name = db.shorten_name(u'core_challenge_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm[u'core.challenge'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['challenge_id', 'person_id'])


    def backwards(self, orm):
        # Adding M2M table for field challenges on 'Person'
        m2m_table_name = db.shorten_name(u'core_person_challenges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False)),
            ('challenge', models.ForeignKey(orm[u'core.challenge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'challenge_id'])

        # Removing M2M table for field participants on 'Challenge'
        db.delete_table(db.shorten_name(u'core_challenge_participants'))


    models = {
        u'core.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants'", 'symmetrical': 'False', 'to': u"orm['core.Person']"}),
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