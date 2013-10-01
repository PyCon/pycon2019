import csv
import logging
import requests

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand

from constance import config

from pycon.models import PyConTutorialProposal


log = logging.getLogger(__name__)


def get_tutorial(cte_id, title, max_attendees):
    """
        Return a Tutorial based on the supplied CTE ID or Title. If there is
        no match against CTE ID, we have not mapped this before, and must
        lookup by Title and update the CTE ID field. In addition, the max
        attendees may have changed based on overall registrants and room.
    """
    try:
        tutorial = PyConTutorialProposal.objects.get(cte_tutorial_id=cte_id)
    except PyConTutorialProposal.DoesNotExist:
        pass
    try:
        tutorial = PyConTutorialProposal.objects.get(title=title)
        tutorial.cte_tutorial_id = cte_id
    except PyConTutorialProposal.DoesNotExist as e:
        log.warn("Could not locate Tutorial by CTE ID: %s or Title: %s" % (cte_id, title))
        raise e
    tutorial.max_attendees = max_attendees
    tutorial.save()
    return tutorial


def get_user(email):
    """
        Return a user object by email lookup
    """
    model = get_user_model()
    return model.objects.get(email=email)


class Command(NoArgsCommand):
    """
        Parses an external CSV for tutorial registrant data and updates the
        corresponding Tutorial instance with registrant information
    """

    def handle_noargs(self, **options):
        """Fetch the external URL and parse the data"""
        url = config.CTE_TUTORIAL_DATA_URL
        req = requests.get(url)
        data = req.content.splitlines()
        # parse the CSV data
        reader = csv.reader(data)

        # CTE ID: PyConTutorialProposal
        tutorials = {}
        # PyConTutorialProposal: [emails,]
        registrant_data = {}
        # Assume no header row
        for row in reader:
            tut_id = row[0]
            title = row[1]
            max_attendees = row[2]
            registrant_email = row[3]
            if tut_id in tutorials:
                tutorial = tutorials[tut_id]
            else:
                tutorial = get_tutorial(tut_id, title, max_attendees)
                tutorials[tut_id] = tutorial
            if tutorial:
                if tutorial in registrant_data:
                    registrant_data[tutorial].append(registrant_email)
                else:
                    registrant_data[tutorial] = [registrant_email]

        # Add the Users objects to the associated Tutorial as registrants
        for tutorial, registrants in registrant_data.items():
            users = get_user_model().objects.filter(email__in=registrants)
            tutorial.registrants.add(*users)
            log.info("Updated %s registrant(s) for %s." % (users.count(), tutorial))
