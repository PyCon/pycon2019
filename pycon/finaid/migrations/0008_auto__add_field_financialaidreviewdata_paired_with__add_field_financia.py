# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FinancialAidReviewData.paired_with'
        db.add_column(u'finaid_financialaidreviewdata', 'paired_with',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.hotel_notes'
        db.add_column(u'finaid_financialaidreviewdata', 'hotel_notes',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.travel_amount'
        db.add_column(u'finaid_financialaidreviewdata', 'travel_amount',
                      self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.tutorial_amount'
        db.add_column(u'finaid_financialaidreviewdata', 'tutorial_amount',
                      self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.registration_amount'
        db.add_column(u'finaid_financialaidreviewdata', 'registration_amount',
                      self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.grant_letter_sent'
        db.add_column(u'finaid_financialaidreviewdata', 'grant_letter_sent',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.cash_check'
        db.add_column(u'finaid_financialaidreviewdata', 'cash_check',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.notes'
        db.add_column(u'finaid_financialaidreviewdata', 'notes',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.travel_signed'
        db.add_column(u'finaid_financialaidreviewdata', 'travel_signed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.travel_cash_check'
        db.add_column(u'finaid_financialaidreviewdata', 'travel_cash_check',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.travel_check_number'
        db.add_column(u'finaid_financialaidreviewdata', 'travel_check_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.travel_preferred_disbursement'
        db.add_column(u'finaid_financialaidreviewdata', 'travel_preferred_disbursement',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'FinancialAidReviewData.promo_code'
        db.add_column(u'finaid_financialaidreviewdata', 'promo_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FinancialAidReviewData.paired_with'
        db.delete_column(u'finaid_financialaidreviewdata', 'paired_with_id')

        # Deleting field 'FinancialAidReviewData.hotel_notes'
        db.delete_column(u'finaid_financialaidreviewdata', 'hotel_notes')

        # Deleting field 'FinancialAidReviewData.travel_amount'
        db.delete_column(u'finaid_financialaidreviewdata', 'travel_amount')

        # Deleting field 'FinancialAidReviewData.tutorial_amount'
        db.delete_column(u'finaid_financialaidreviewdata', 'tutorial_amount')

        # Deleting field 'FinancialAidReviewData.registration_amount'
        db.delete_column(u'finaid_financialaidreviewdata', 'registration_amount')

        # Deleting field 'FinancialAidReviewData.grant_letter_sent'
        db.delete_column(u'finaid_financialaidreviewdata', 'grant_letter_sent')

        # Deleting field 'FinancialAidReviewData.cash_check'
        db.delete_column(u'finaid_financialaidreviewdata', 'cash_check')

        # Deleting field 'FinancialAidReviewData.notes'
        db.delete_column(u'finaid_financialaidreviewdata', 'notes')

        # Deleting field 'FinancialAidReviewData.travel_signed'
        db.delete_column(u'finaid_financialaidreviewdata', 'travel_signed')

        # Deleting field 'FinancialAidReviewData.travel_cash_check'
        db.delete_column(u'finaid_financialaidreviewdata', 'travel_cash_check')

        # Deleting field 'FinancialAidReviewData.travel_check_number'
        db.delete_column(u'finaid_financialaidreviewdata', 'travel_check_number')

        # Deleting field 'FinancialAidReviewData.travel_preferred_disbursement'
        db.delete_column(u'finaid_financialaidreviewdata', 'travel_preferred_disbursement')

        # Deleting field 'FinancialAidReviewData.promo_code'
        db.delete_column(u'finaid_financialaidreviewdata', 'promo_code')


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
            'hotel_arrival_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'hotel_departure_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
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
        },
        u'finaid.financialaidreviewdata': {
            'Meta': {'object_name': 'FinancialAidReviewData'},
            'application': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'review'", 'unique': 'True', 'to': u"orm['finaid.FinancialAidApplication']"}),
            'cash_check': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grant_letter_sent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hotel_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'hotel_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paired_with': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'promo_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'registration_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'travel_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'travel_cash_check': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'travel_check_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'travel_preferred_disbursement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'travel_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tutorial_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'})
        }
    }

    complete_apps = ['finaid']