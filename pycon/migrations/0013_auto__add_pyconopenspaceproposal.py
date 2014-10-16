# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PyConOpenSpaceProposal'
        db.create_table(u'pycon_pyconopenspaceproposal', (
            (u'proposalbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['proposals.ProposalBase'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pycon.PyConProposalCategory'])),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('overall_status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('damaged_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rejection_status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('recording_release', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('additional_requirements', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'pycon', ['PyConOpenSpaceProposal'])


    def backwards(self, orm):
        # Deleting model 'PyConOpenSpaceProposal'
        db.delete_table(u'pycon_pyconopenspaceproposal')


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
        u'conference.section': {
            'Meta': {'object_name': 'Section'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.Conference']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'proposals.additionalspeaker': {
            'Meta': {'unique_together': "(('speaker', 'proposalbase'),)", 'object_name': 'AdditionalSpeaker', 'db_table': "'proposals_proposalbase_additional_speakers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposalbase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalBase']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['speakers.Speaker']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'proposals.proposalbase': {
            'Meta': {'object_name': 'ProposalBase'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'additional_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['speakers.Speaker']", 'symmetrical': 'False', 'through': u"orm['proposals.AdditionalSpeaker']", 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': u"orm['speakers.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'proposals.proposalkind': {
            'Meta': {'object_name': 'ProposalKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposal_kinds'", 'to': u"orm['conference.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'pycon.pyconlightningtalkproposal': {
            'Meta': {'object_name': 'PyConLightningTalkProposal'},
            'additional_requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pycon.PyConProposalCategory']"}),
            'damaged_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rejection_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pycon.pyconopenspaceproposal': {
            'Meta': {'object_name': 'PyConOpenSpaceProposal'},
            'additional_requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pycon.PyConProposalCategory']"}),
            'damaged_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rejection_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pycon.pyconposterproposal': {
            'Meta': {'object_name': 'PyConPosterProposal'},
            'additional_requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pycon.PyConProposalCategory']"}),
            'damaged_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rejection_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pycon.pyconproposalcategory': {
            'Meta': {'object_name': 'PyConProposalCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'pycon.pyconsponsortutorialproposal': {
            'Meta': {'object_name': 'PyConSponsorTutorialProposal', '_ormbases': [u'proposals.ProposalBase']},
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'pycon.pycontalkproposal': {
            'Meta': {'object_name': 'PyConTalkProposal'},
            'additional_requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pycon.PyConProposalCategory']"}),
            'damaged_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'outline': ('django.db.models.fields.TextField', [], {}),
            'overall_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'perceived_value': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rejection_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thunderdome_group': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'talks'", 'null': 'True', 'blank': 'True', 'to': u"orm['pycon.ThunderdomeGroup']"})
        },
        u'pycon.pycontutorialproposal': {
            'Meta': {'object_name': 'PyConTutorialProposal'},
            'additional_requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pycon.PyConProposalCategory']"}),
            'cte_tutorial_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'damaged_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'domain_level': ('django.db.models.fields.IntegerField', [], {}),
            'handout': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_attendees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'more_info': ('django.db.models.fields.TextField', [], {}),
            'outline': ('django.db.models.fields.TextField', [], {}),
            'overall_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'perceived_value': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            u'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'registrants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'rejection_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pycon.thunderdomegroup': {
            'Meta': {'object_name': 'ThunderdomeGroup'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'decided': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'speakers.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sessions_preference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['pycon']