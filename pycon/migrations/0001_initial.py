# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PyConProposalCategory'
        db.create_table('pycon_pyconproposalcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('pycon', ['PyConProposalCategory'])

        # Adding model 'PyConTalkProposal'
        db.create_table('pycon_pycontalkproposal', (
            ('proposalbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['proposals.ProposalBase'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pycon.PyConProposalCategory'])),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('recording_release', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('extreme', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('pycon', ['PyConTalkProposal'])

        # Adding model 'PyConTutorialProposal'
        db.create_table('pycon_pycontutorialproposal', (
            ('proposalbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['proposals.ProposalBase'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pycon.PyConProposalCategory'])),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('recording_release', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('pycon', ['PyConTutorialProposal'])

        # Adding model 'PyConPosterProposal'
        db.create_table('pycon_pyconposterproposal', (
            ('proposalbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['proposals.ProposalBase'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pycon.PyConProposalCategory'])),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('recording_release', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('pycon', ['PyConPosterProposal'])

        # Adding model 'PyConSponsorTutorialProposal'
        db.create_table('pycon_pyconsponsortutorialproposal', (
            ('proposalbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['proposals.ProposalBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('pycon', ['PyConSponsorTutorialProposal'])


    def backwards(self, orm):
        # Deleting model 'PyConProposalCategory'
        db.delete_table('pycon_pyconproposalcategory')

        # Deleting model 'PyConTalkProposal'
        db.delete_table('pycon_pycontalkproposal')

        # Deleting model 'PyConTutorialProposal'
        db.delete_table('pycon_pycontutorialproposal')

        # Deleting model 'PyConPosterProposal'
        db.delete_table('pycon_pyconposterproposal')

        # Deleting model 'PyConSponsorTutorialProposal'
        db.delete_table('pycon_pyconsponsortutorialproposal')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'conference.conference': {
            'Meta': {'object_name': 'Conference'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('timezones.fields.TimeZoneField', [], {'default': "'US/Eastern'", 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.section': {
            'Meta': {'object_name': 'Section'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Conference']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposals.additionalspeaker': {
            'Meta': {'unique_together': "(('speaker', 'proposalbase'),)", 'object_name': 'AdditionalSpeaker', 'db_table': "'proposals_proposalbase_additional_speakers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposalbase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposals.ProposalBase']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['speakers.Speaker']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'proposals.proposalbase': {
            'Meta': {'object_name': 'ProposalBase'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_additional_notes_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_notes': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['speakers.Speaker']", 'symmetrical': 'False', 'through': "orm['proposals.AdditionalSpeaker']", 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposals.ProposalKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': "orm['speakers.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposals.proposalkind': {
            'Meta': {'object_name': 'ProposalKind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposal_kinds'", 'to': "orm['conference.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'pycon.pyconposterproposal': {
            'Meta': {'object_name': 'PyConPosterProposal'},
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pycon.PyConProposalCategory']"}),
            'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'pycon.pyconproposalcategory': {
            'Meta': {'object_name': 'PyConProposalCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'pycon.pyconsponsortutorialproposal': {
            'Meta': {'object_name': 'PyConSponsorTutorialProposal', '_ormbases': ['proposals.ProposalBase']},
            'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'pycon.pycontalkproposal': {
            'Meta': {'object_name': 'PyConTalkProposal'},
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pycon.PyConProposalCategory']"}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extreme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'pycon.pycontutorialproposal': {
            'Meta': {'object_name': 'PyConTutorialProposal'},
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pycon.PyConProposalCategory']"}),
            'proposalbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['proposals.ProposalBase']", 'unique': 'True', 'primary_key': 'True'}),
            'recording_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'speakers.speaker': {
            'Meta': {'object_name': 'Speaker'},
            '_biography_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sessions_preference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['pycon']