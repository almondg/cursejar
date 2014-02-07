# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding model 'PayPalUser'
        db.create_table(u'core_paypaluser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('pre_approval_key', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'core', ['PayPalUser'])

        # Adding model 'Challenge'
        db.create_table(u'core_challenge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID')),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 14, 0, 0))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('word1', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('word2', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('word3', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Challenge'])

        # Adding M2M table for field participant on 'Challenge'
        m2m_table_name = db.shorten_name(u'core_challenge_participant')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm[u'core.challenge'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['challenge_id', 'person_id'])

        # Adding model 'Jar'
        db.create_table(u'core_jar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jar', to=orm['core.Challenge'])),
            ('current_sum', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Jar'])

        # Adding model 'ChargeEvent'
        db.create_table(u'core_chargeevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Jar'])),
            ('date_of_felony', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('felon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('crime', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('evidence', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'core', ['ChargeEvent'])

        # Adding model 'Word'
        db.create_table(u'core_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Challenge'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fine', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'core', ['Word'])

        # Adding unique constraint on 'Word', fields ['name', 'challenge']
        db.create_unique(u'core_word', ['name', 'challenge_id'])

        # Adding model 'UserProfile'
        db.create_table('user_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID')),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', null=True, to=orm['core.Person'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['UserProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Word', fields ['name', 'challenge']
        db.delete_unique(u'core_word', ['name', 'challenge_id'])

        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Deleting model 'PayPalUser'
        db.delete_table(u'core_paypaluser')

        # Deleting model 'Challenge'
        db.delete_table(u'core_challenge')

        # Removing M2M table for field participant on 'Challenge'
        db.delete_table(db.shorten_name(u'core_challenge_participant'))

        # Deleting model 'Jar'
        db.delete_table(u'core_jar')

        # Deleting model 'ChargeEvent'
        db.delete_table(u'core_chargeevent')

        # Deleting model 'Word'
        db.delete_table(u'core_word')

        # Deleting model 'UserProfile'
        db.delete_table('user_profile')


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
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jar'", 'to': u"orm['core.Challenge']"}),
            'current_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.paypaluser': {
            'Meta': {'object_name': 'PayPalUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'pre_approval_key': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
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