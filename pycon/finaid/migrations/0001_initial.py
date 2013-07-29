# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FinancialAidApplication'
        db.create_table(u'finaid_financialaidapplication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='financial_aid', unique=True, to=orm['auth.User'])),
            ('pyladies_grant_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_grant_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hotel_grant_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hotel_nights', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('travel_grant_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('international', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('travel_amount_requested', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
            ('travel_plans', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('tutorial_grant_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('involvement', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('what_you_want', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('want_to_learn', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('portfolios', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('use_of_python', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('beginner_resources', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('presenting', self.gf('django.db.models.fields.IntegerField')()),
            ('experience_level', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('presented', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'finaid', ['FinancialAidApplication'])


    def backwards(self, orm):
        # Deleting model 'FinancialAidApplication'
        db.delete_table(u'finaid_financialaidapplication')


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
            'hotel_grant_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hotel_nights': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'involvement': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['finaid']