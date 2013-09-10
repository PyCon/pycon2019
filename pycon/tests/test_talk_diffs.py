import json

from django.test import TestCase

from pycon.models import TalkProposalDiff

from .factories import PyConTalkProposalFactory


class DiffTests(TestCase):

    def test_no_diff_on_create(self):
        talk = PyConTalkProposalFactory.create()
        with self.assertRaises(TalkProposalDiff.DoesNotExist):
            TalkProposalDiff.objects.get(talk=talk)

    def test_diff_created_on_edit(self):
        talk = PyConTalkProposalFactory.create()
        talk.abstract = "foo"
        talk.save()
        diff = TalkProposalDiff.objects.get(talk=talk)
        diff_dict = json.loads(diff.diffs_json)
        self.assertTrue("foo" in diff_dict['abstract'])
