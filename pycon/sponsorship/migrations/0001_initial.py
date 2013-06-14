# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SponsorLevel'
        db.create_table(u'sponsorship_sponsorlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Conference'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sponsorship', ['SponsorLevel'])

        # Adding model 'Sponsor'
        db.create_table(u'sponsorship_sponsor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sponsorships', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('display_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('external_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('annotation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sponsorship.SponsorLevel'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sponsor_logo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['sponsorship.SponsorBenefit'])),
        ))
        db.send_create_signal(u'sponsorship', ['Sponsor'])

        # Adding model 'Benefit'
        db.create_table(u'sponsorship_benefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='simple', max_length=10)),
        ))
        db.send_create_signal(u'sponsorship', ['Benefit'])

        # Adding model 'BenefitLevel'
        db.create_table(u'sponsorship_benefitlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('benefit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='benefit_levels', to=orm['sponsorship.Benefit'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(related_name='benefit_levels', to=orm['sponsorship.SponsorLevel'])),
            ('max_words', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('other_limits', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'sponsorship', ['BenefitLevel'])

        # Adding model 'SponsorBenefit'
        db.create_table(u'sponsorship_sponsorbenefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sponsor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sponsor_benefits', to=orm['sponsorship.Sponsor'])),
            ('benefit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sponsor_benefits', to=orm['sponsorship.Benefit'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_words', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('other_limits', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('upload', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'sponsorship', ['SponsorBenefit'])


    def backwards(self, orm):
        # Deleting model 'SponsorLevel'
        db.delete_table(u'sponsorship_sponsorlevel')

        # Deleting model 'Sponsor'
        db.delete_table(u'sponsorship_sponsor')

        # Deleting model 'Benefit'
        db.delete_table(u'sponsorship_benefit')

        # Deleting model 'BenefitLevel'
        db.delete_table(u'sponsorship_benefitlevel')

        # Deleting model 'SponsorBenefit'
        db.delete_table(u'sponsorship_sponsorbenefit')


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
            'Meta': {'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsorships'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sponsorship.SponsorLevel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsor_logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['sponsorship.SponsorBenefit']"})
        },
        u'sponsorship.sponsorbenefit': {
            'Meta': {'ordering': "['-active']", 'object_name': 'SponsorBenefit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': u"orm['sponsorship.Benefit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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