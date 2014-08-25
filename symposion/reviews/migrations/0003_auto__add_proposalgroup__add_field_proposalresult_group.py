# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProposalGroup'
        db.create_table(u'reviews_proposalgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('review_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('vote_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('vote_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'reviews', ['ProposalGroup'])

        # Adding field 'ProposalResult.group'
        db.add_column(u'reviews_proposalresult', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proposal_results', null=True, to=orm['reviews.ProposalGroup']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProposalGroup'
        db.delete_table(u'reviews_proposalgroup')

        # Deleting field 'ProposalResult.group'
        db.delete_column(u'reviews_proposalresult', 'group_id')


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
        u'reviews.comment': {
            'Meta': {'object_name': 'Comment'},
            'commented_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'commenter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['proposals.ProposalBase']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'reviews.latestvote': {
            'Meta': {'unique_together': "[('proposal', 'user')]", 'object_name': 'LatestVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'reviews.notificationtemplate': {
            'Meta': {'object_name': 'NotificationTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.proposalgroup': {
            'Meta': {'object_name': 'ProposalGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'review_start': ('django.db.models.fields.DateTimeField', [], {}),
            'vote_end': ('django.db.models.fields.DateTimeField', [], {}),
            'vote_start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'reviews.proposalmessage': {
            'Meta': {'ordering': "['submitted_at']", 'object_name': 'ProposalMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': u"orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'reviews.proposalresult': {
            'Meta': {'object_name': 'ProposalResult'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proposal_results'", 'null': 'True', 'to': u"orm['reviews.ProposalGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minus_one': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minus_zero': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'plus_one': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'plus_zero': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'proposal': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'result'", 'unique': 'True', 'to': u"orm['proposals.ProposalBase']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '5', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'undecided'", 'max_length': '20', 'db_index': 'True'}),
            'vote_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'reviews.resultnotification': {
            'Meta': {'object_name': 'ResultNotification'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': u"orm['proposals.ProposalBase']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.NotificationTemplate']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'to_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['proposals.ProposalBase']"}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'reviews.reviewassignment': {
            'Meta': {'object_name': 'ReviewAssignment'},
            'assigned_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opted_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin': ('django.db.models.fields.IntegerField', [], {}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['proposals.ProposalBase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'speakers.speaker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Speaker'},
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

    complete_apps = ['reviews']