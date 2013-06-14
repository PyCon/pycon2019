# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table(u'schedule_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['conference.Section'], unique=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'schedule', ['Schedule'])

        # Adding model 'Day'
        db.create_table(u'schedule_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'schedule', ['Day'])

        # Adding unique constraint on 'Day', fields ['schedule', 'date']
        db.create_unique(u'schedule_day', ['schedule_id', 'date'])

        # Adding model 'Room'
        db.create_table(u'schedule_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'schedule', ['Room'])

        # Adding model 'SlotKind'
        db.create_table(u'schedule_slotkind', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Schedule'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'schedule', ['SlotKind'])

        # Adding model 'Slot'
        db.create_table(u'schedule_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Day'])),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.SlotKind'])),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('content_override', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'schedule', ['Slot'])

        # Adding model 'SlotRoom'
        db.create_table(u'schedule_slotroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Slot'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Room'])),
        ))
        db.send_create_signal(u'schedule', ['SlotRoom'])

        # Adding unique constraint on 'SlotRoom', fields ['slot', 'room']
        db.create_unique(u'schedule_slotroom', ['slot_id', 'room_id'])

        # Adding model 'Presentation'
        db.create_table(u'schedule_presentation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='content_ptr', unique=True, null=True, to=orm['schedule.Slot'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('abstract', self.gf('django.db.models.fields.TextField')()),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presentations', to=orm['speakers.Speaker'])),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('proposal_base', self.gf('django.db.models.fields.related.OneToOneField')(related_name='presentation', unique=True, to=orm['proposals.ProposalBase'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presentations', to=orm['conference.Section'])),
        ))
        db.send_create_signal(u'schedule', ['Presentation'])

        # Adding M2M table for field additional_speakers on 'Presentation'
        m2m_table_name = db.shorten_name(u'schedule_presentation_additional_speakers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentation', models.ForeignKey(orm[u'schedule.presentation'], null=False)),
            ('speaker', models.ForeignKey(orm[u'speakers.speaker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['presentation_id', 'speaker_id'])

        # Adding model 'Session'
        db.create_table(u'schedule_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['schedule.Day'])),
        ))
        db.send_create_signal(u'schedule', ['Session'])

        # Adding M2M table for field slots on 'Session'
        m2m_table_name = db.shorten_name(u'schedule_session_slots')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'schedule.session'], null=False)),
            ('slot', models.ForeignKey(orm[u'schedule.slot'], null=False))
        ))
        db.create_unique(m2m_table_name, ['session_id', 'slot_id'])

        # Adding model 'SessionRole'
        db.create_table(u'schedule_sessionrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Session'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'schedule', ['SessionRole'])

        # Adding unique constraint on 'SessionRole', fields ['session', 'user', 'role']
        db.create_unique(u'schedule_sessionrole', ['session_id', 'user_id', 'role'])


    def backwards(self, orm):
        # Removing unique constraint on 'SessionRole', fields ['session', 'user', 'role']
        db.delete_unique(u'schedule_sessionrole', ['session_id', 'user_id', 'role'])

        # Removing unique constraint on 'SlotRoom', fields ['slot', 'room']
        db.delete_unique(u'schedule_slotroom', ['slot_id', 'room_id'])

        # Removing unique constraint on 'Day', fields ['schedule', 'date']
        db.delete_unique(u'schedule_day', ['schedule_id', 'date'])

        # Deleting model 'Schedule'
        db.delete_table(u'schedule_schedule')

        # Deleting model 'Day'
        db.delete_table(u'schedule_day')

        # Deleting model 'Room'
        db.delete_table(u'schedule_room')

        # Deleting model 'SlotKind'
        db.delete_table(u'schedule_slotkind')

        # Deleting model 'Slot'
        db.delete_table(u'schedule_slot')

        # Deleting model 'SlotRoom'
        db.delete_table(u'schedule_slotroom')

        # Deleting model 'Presentation'
        db.delete_table(u'schedule_presentation')

        # Removing M2M table for field additional_speakers on 'Presentation'
        db.delete_table(db.shorten_name(u'schedule_presentation_additional_speakers'))

        # Deleting model 'Session'
        db.delete_table(u'schedule_session')

        # Removing M2M table for field slots on 'Session'
        db.delete_table(db.shorten_name(u'schedule_session_slots'))

        # Deleting model 'SessionRole'
        db.delete_table(u'schedule_sessionrole')


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
        u'schedule.day': {
            'Meta': {'unique_together': "[('schedule', 'date')]", 'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Schedule']"})
        },
        u'schedule.presentation': {
            'Meta': {'ordering': "['slot']", 'object_name': 'Presentation'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'copresentations'", 'blank': 'True', 'to': u"orm['speakers.Speaker']"}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proposal_base': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'presentation'", 'unique': 'True', 'to': u"orm['proposals.ProposalBase']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': u"orm['conference.Section']"}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'content_ptr'", 'unique': 'True', 'null': 'True', 'to': u"orm['schedule.Slot']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'presentations'", 'to': u"orm['speakers.Speaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'schedule.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Schedule']"})
        },
        u'schedule.schedule': {
            'Meta': {'object_name': 'Schedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'section': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['conference.Section']", 'unique': 'True'})
        },
        u'schedule.session': {
            'Meta': {'object_name': 'Session'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': u"orm['schedule.Day']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slots': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sessions'", 'symmetrical': 'False', 'to': u"orm['schedule.Slot']"})
        },
        u'schedule.sessionrole': {
            'Meta': {'unique_together': "[('session', 'user', 'role')]", 'object_name': 'SessionRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Session']"}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'schedule.slot': {
            'Meta': {'ordering': "['day', 'start', 'end']", 'object_name': 'Slot'},
            'content_override': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.SlotKind']"}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        u'schedule.slotkind': {
            'Meta': {'object_name': 'SlotKind'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Schedule']"})
        },
        u'schedule.slotroom': {
            'Meta': {'ordering': "['slot', 'room__order']", 'unique_together': "[('slot', 'room')]", 'object_name': 'SlotRoom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Room']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.Slot']"})
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
        }
    }

    complete_apps = ['schedule']