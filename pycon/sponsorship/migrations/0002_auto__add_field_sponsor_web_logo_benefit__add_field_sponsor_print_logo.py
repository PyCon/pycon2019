# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sponsor.web_logo_benefit'
        db.add_column(u'sponsorship_sponsor', 'web_logo_benefit',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sponsor.print_logo_benefit'
        db.add_column(u'sponsorship_sponsor', 'print_logo_benefit',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sponsor.print_description_benefit'
        db.add_column(u'sponsorship_sponsor', 'print_description_benefit',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sponsor.company_description_benefit'
        db.add_column(u'sponsorship_sponsor', 'company_description_benefit',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sponsor.advertisement_benefit'
        db.add_column(u'sponsorship_sponsor', 'advertisement_benefit',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SponsorBenefit.is_complete'
        db.add_column(u'sponsorship_sponsorbenefit', 'is_complete',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sponsor.web_logo_benefit'
        db.delete_column(u'sponsorship_sponsor', 'web_logo_benefit')

        # Deleting field 'Sponsor.print_logo_benefit'
        db.delete_column(u'sponsorship_sponsor', 'print_logo_benefit')

        # Deleting field 'Sponsor.print_description_benefit'
        db.delete_column(u'sponsorship_sponsor', 'print_description_benefit')

        # Deleting field 'Sponsor.company_description_benefit'
        db.delete_column(u'sponsorship_sponsor', 'company_description_benefit')

        # Deleting field 'Sponsor.advertisement_benefit'
        db.delete_column(u'sponsorship_sponsor', 'advertisement_benefit')

        # Deleting field 'SponsorBenefit.is_complete'
        db.delete_column(u'sponsorship_sponsorbenefit', 'is_complete')


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
        u'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'US/Eastern'", 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sponsorship.benefit': {
            'Meta': {'object_name': 'Benefit'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'})
        },
        u'sponsorship.benefitlevel': {
            'Meta': {'ordering': "['level']", 'object_name': 'BenefitLevel'},
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'benefit_levels'", 'to': u"orm['sponsorship.Benefit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'benefit_levels'", 'to': u"orm['sponsorship.SponsorLevel']"}),
            'max_words': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_limits': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'sponsorship.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'advertisement_benefit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsorships'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'company_description_benefit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sponsorship.SponsorLevel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'print_description_benefit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'print_logo_benefit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sponsor_logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['sponsorship.SponsorBenefit']"}),
            'web_logo_benefit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sponsorship.sponsorbenefit': {
            'Meta': {'ordering': "['-active']", 'object_name': 'SponsorBenefit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': u"orm['sponsorship.Benefit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'max_words': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_limits': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': u"orm['sponsorship.Sponsor']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'sponsorship.sponsorlevel': {
            'Meta': {'ordering': "['conference', 'order']", 'object_name': 'SponsorLevel'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.Conference']"}),
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['sponsorship']
