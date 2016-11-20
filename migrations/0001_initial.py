# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import dbs
from south.v2 import SchemaMigration
from django.db import models

db = dbs['datastore']

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HashtagStatus'
        db.create_table(u'geonodetwitter_hashtagstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashtag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('is_listening', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'geonodetwitter', ['HashtagStatus'])

        # Adding model 'Tweet'
        db.create_table(u'geonodetwitter_tweet', (
            ('id_str', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('hashtag', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('coordinates_lon', self.gf('django.db.models.fields.FloatField')()),
            ('coordinates_lat', self.gf('django.db.models.fields.FloatField')()),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('radius', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('media_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('geonodetwitter', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'HashtagStatus'
        db.delete_table(u'geonodetwitter_hashtagstatus')

        # Deleting model 'Tweet'
        db.delete_table(u'geonodetwitter_tweet')


    models = {
        u'geonodetwitter.hashtagstatus': {
            'Meta': {'object_name': 'HashtagStatus'},
            'hashtag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_listening': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'geonodetwitter.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'coordinates_lat': ('django.db.models.fields.FloatField', [], {}),
            'coordinates_lon': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'hashtag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id_str': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'media_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['geonodetwitter']