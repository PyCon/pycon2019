from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from .models import Membership, Team


class TestTeamPermissions(TestCase):
    # We create a user, a team, and two perms.  The team
    # gets one perm for members and the other for managers.
    # The tests add the user to the team in various ways and
    # check what permissions they end up with.

    def setUp(self):
        ct = ContentType.objects.get_for_model(Team)
        self.user1 = User.objects.create_user('user1')
        self.team1 = Team.objects.create(slug='1', name='team1')

        self.perm1 = Permission.objects.create(name='perm1', codename='perm1',
                                               content_type=ct)
        self.perm1.name = u"%s.%s" % (ct.app_label, self.perm1.codename)

        self.perm2 = Permission.objects.create(name='perm2', codename='perm2',
                                               content_type=ct)
        self.perm2.name = u"%s.%s" % (ct.app_label, self.perm2.codename)

        self.team1.permissions.add(self.perm1)
        self.team1.manager_permissions.add(self.perm2)

    def test_not_on_team(self):
        # No permissions
        self.assertFalse(self.user1.has_perm(self.perm1.name))
        self.assertFalse(self.user1.has_perm(self.perm2.name))

    def test_invited_to_team(self):
        # Invited but not on the team, no permissions still
        Membership.objects.create(user=self.user1, team=self.team1,
                                  state='invited')
        self.assertFalse(self.user1.has_perm(self.perm1.name))
        self.assertFalse(self.user1.has_perm(self.perm2.name))

    def test_team_member(self):
        # Member permissions, not manager permissions
        Membership.objects.create(user=self.user1, team=self.team1,
                                  state='member')
        self.assertTrue(self.user1.has_perm(self.perm1.name))
        self.assertFalse(self.user1.has_perm(self.perm2.name))

    def test_team_manager(self):
        # Both member and manager permissions
        Membership.objects.create(user=self.user1, team=self.team1,
                                  state='manager')
        self.assertTrue(self.user1.has_perm(self.perm1.name))
        self.assertTrue(self.user1.has_perm(self.perm2.name))
