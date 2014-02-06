# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Challenge'
        db.create_table(u'core_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default='in_a_week_from_now')),
        ))
        db.send_create_signal(u'core', ['Challenge'])

        # Adding model 'Jar'
        db.create_table(u'core_jar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Challenge'])),
            ('current_sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['Jar'])

        # Adding model 'ChargeEvent'
        db.create_table(u'core_chargeevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Jar'])),
            ('date_of_felony', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('felon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('crime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Word'])),
            ('evidence', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'core', ['ChargeEvent'])

        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding M2M table for field challenges on 'Person'
        m2m_table_name = db.shorten_name(u'core_person_challenges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False)),
            ('challenge', models.ForeignKey(orm[u'core.challenge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'challenge_id'])

        # Adding model 'Word'
        db.create_table(u'core_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Challenge'])),
            ('fine', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'core', ['Word'])


    def backwards(self, orm):
        # Deleting model 'Challenge'
        db.delete_table(u'core_challenge')

        # Deleting model 'Jar'
        db.delete_table(u'core_jar')

        # Deleting model 'ChargeEvent'
        db.delete_table(u'core_chargeevent')

        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Removing M2M table for field challenges on 'Person'
        db.delete_table(db.shorten_name(u'core_person_challenges'))

        # Deleting model 'Word'
        db.delete_table(u'core_word')


    models = {
        u'core.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': "'in_a_week_from_now'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'challenges': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants'", 'symmetrical': 'False', 'to': u"orm['core.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.word': {
            'Meta': {'object_name': 'Word'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Challenge']"}),
            'fine': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['core']