# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OpeningHours'
        db.create_table(u'gmp_databases_openinghours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('open', self.gf('django.db.models.fields.TimeField')()),
            ('close', self.gf('django.db.models.fields.TimeField')(null=True)),
        ))
        db.send_create_signal(u'gmp_databases', ['OpeningHours'])

        # Adding model 'Type'
        db.create_table(u'gmp_databases_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'gmp_databases', ['Type'])

        # Adding model 'Country'
        db.create_table(u'gmp_databases_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'gmp_databases', ['Country'])

        # Adding model 'Street'
        db.create_table(u'gmp_databases_street', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'gmp_databases', ['Street'])

        # Adding model 'City'
        db.create_table(u'gmp_databases_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'gmp_databases', ['City'])

        # Adding model 'Location'
        db.create_table(u'gmp_databases_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=12)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=12)),
            ('formatted_address', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Country'], null=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.City'], null=True)),
        ))
        db.send_create_signal(u'gmp_databases', ['Location'])

        # Adding model 'Place'
        db.create_table(u'gmp_databases_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Location'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
        ))
        db.send_create_signal(u'gmp_databases', ['Place'])

        # Adding M2M table for field types on 'Place'
        m2m_table_name = db.shorten_name(u'gmp_databases_place_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm[u'gmp_databases.place'], null=False)),
            ('type', models.ForeignKey(orm[u'gmp_databases.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['place_id', 'type_id'])

        # Adding M2M table for field opening_hours on 'Place'
        m2m_table_name = db.shorten_name(u'gmp_databases_place_opening_hours')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm[u'gmp_databases.place'], null=False)),
            ('openinghours', models.ForeignKey(orm[u'gmp_databases.openinghours'], null=False))
        ))
        db.create_unique(m2m_table_name, ['place_id', 'openinghours_id'])

        # Adding model 'Review'
        db.create_table(u'gmp_databases_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=1)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Place'])),
        ))
        db.send_create_signal(u'gmp_databases', ['Review'])

        # Adding model 'Image'
        db.create_table(u'gmp_databases_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Place'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'gmp_databases', ['Image'])

        # Adding model 'HistoryParams'
        db.create_table(u'gmp_databases_historyparams', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opening_hours', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.OpeningHours'])),
            ('place_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Type'])),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=1)),
        ))
        db.send_create_signal(u'gmp_databases', ['HistoryParams'])

        # Adding model 'User'
        db.create_table(u'gmp_databases_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gmp_databases.Location'])),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'gmp_databases', ['User'])

        # Adding M2M table for field history_params on 'User'
        m2m_table_name = db.shorten_name(u'gmp_databases_user_history_params')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'gmp_databases.user'], null=False)),
            ('historyparams', models.ForeignKey(orm[u'gmp_databases.historyparams'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'historyparams_id'])


    def backwards(self, orm):
        # Deleting model 'OpeningHours'
        db.delete_table(u'gmp_databases_openinghours')

        # Deleting model 'Type'
        db.delete_table(u'gmp_databases_type')

        # Deleting model 'Country'
        db.delete_table(u'gmp_databases_country')

        # Deleting model 'Street'
        db.delete_table(u'gmp_databases_street')

        # Deleting model 'City'
        db.delete_table(u'gmp_databases_city')

        # Deleting model 'Location'
        db.delete_table(u'gmp_databases_location')

        # Deleting model 'Place'
        db.delete_table(u'gmp_databases_place')

        # Removing M2M table for field types on 'Place'
        db.delete_table(db.shorten_name(u'gmp_databases_place_types'))

        # Removing M2M table for field opening_hours on 'Place'
        db.delete_table(db.shorten_name(u'gmp_databases_place_opening_hours'))

        # Deleting model 'Review'
        db.delete_table(u'gmp_databases_review')

        # Deleting model 'Image'
        db.delete_table(u'gmp_databases_image')

        # Deleting model 'HistoryParams'
        db.delete_table(u'gmp_databases_historyparams')

        # Deleting model 'User'
        db.delete_table(u'gmp_databases_user')

        # Removing M2M table for field history_params on 'User'
        db.delete_table(db.shorten_name(u'gmp_databases_user_history_params'))


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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gmp_databases.Country']", 'null': 'True'}),
            'formatted_address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '12'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '12'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'gmp_databases.openinghours': {
            'Meta': {'object_name': 'OpeningHours'},
            'close': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
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
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gmp_databases.Type']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'})
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