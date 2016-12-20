# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Location.street'
        db.delete_column(u'gmp_databases_location', 'street_id')


    def backwards(self, orm):
        # Adding field 'Location.street'
        db.add_column(u'gmp_databases_location', 'street',
                      self.gf('django.db.models.fields.related.OneToOneField')(default='', to=orm['gmp_databases.Street'], unique=True),
                      keep_default=False)


    models = {
        u'gmp_databases.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gmp_databases.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gmp_databases.historyparams': {
            'Meta': {'object_name': 'HistoryParams'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opening_hours': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.OpeningHours']"}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Type']"}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'})
        },
        u'gmp_databases.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Place']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'gmp_databases.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['gmp_databases.City']", 'unique': 'True'}),
            'country': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['gmp_databases.Country']", 'unique': 'True'}),
            'formatted_address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '12'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '12'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'gmp_databases.openinghours': {
            'Meta': {'object_name': 'OpeningHours'},
            'close': ('django.db.models.fields.TimeField', [], {}),
            'day': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open': ('django.db.models.fields.TimeField', [], {})
        },
        u'gmp_databases.place': {
            'Meta': {'object_name': 'Place'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'opening_hours': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gmp_databases.OpeningHours']", 'symmetrical': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gmp_databases.Type']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gmp_databases.review': {
            'Meta': {'object_name': 'Review'},
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Place']"}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'gmp_databases.street': {
            'Meta': {'object_name': 'Street'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gmp_databases.type': {
            'Meta': {'object_name': 'Type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'gmp_databases.user': {
            'Meta': {'object_name': 'User'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'history_params': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gmp_databases.HistoryParams']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Location']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['gmp_databases']