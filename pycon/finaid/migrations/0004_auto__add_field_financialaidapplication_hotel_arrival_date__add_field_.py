# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FinancialAidApplication.hotel_arrival_date'
        db.add_column(u'finaid_financialaidapplication', 'hotel_arrival_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 25, 0, 0)),
                      keep_default=False)

        # Adding field 'FinancialAidApplication.hotel_departure_date'
        db.add_column(u'finaid_financialaidapplication', 'hotel_departure_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 25, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FinancialAidApplication.hotel_arrival_date'
        db.delete_column(u'finaid_financialaidapplication', 'hotel_arrival_date')

        # Deleting field 'FinancialAidApplication.hotel_departure_date'
        db.delete_column(u'finaid_financialaidapplication', 'hotel_departure_date')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'finaid.financialaidapplication': {
            'Meta': {'object_name': 'FinancialAidApplication'},
            'beginner_resources': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'experience_level': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hotel_arrival_date': ('django.db.models.fields.DateField', [], {}),
            'hotel_departure_date': ('django.db.models.fields.DateField', [], {}),
            'hotel_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hotel_nights': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'involvement': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'portfolios': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'presented': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'presenting': ('django.db.models.fields.IntegerField', [], {}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pyladies_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sex': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'travel_amount_requested': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'travel_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'travel_plans': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'tutorial_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_of_python': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'financial_aid'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'want_to_learn': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'what_you_want': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'finaid.financialaidapplicationperiod': {
            'Meta': {'object_name': 'FinancialAidApplicationPeriod'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'finaid.financialaidmessage': {
            'Meta': {'ordering': "['submitted_at']", 'object_name': 'FinancialAidMessage'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': u"orm['finaid.FinancialAidApplication']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['finaid']