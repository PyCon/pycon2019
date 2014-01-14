import csv
import logging
import requests

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand

from constance import config

from pycon.models import PyConTutorialProposal


log = logging.getLogger(__name__)


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
        user = config.CTE_BASICAUTH_USER
        pword = config.CTE_BASICAUTH_PASS
        if user and pword:
            req = requests.get(url, auth=(user, pword))
        else:
            req = requests.get(url)
        if not req.raise_for_status():
            data = req.content.splitlines()
            # parse the CSV data
            reader = csv.reader(data)
            # CTE ID: PyConTutorialProposal
            tutorials = {}
            # PyConTutorialProposal: [emails,]
            registrant_data = {}
            # pop header row
            reader.next()
            for row in reader:
                if row:
                    tut_id = row[0]
                    max_attendees = row[2].strip() or None
                    registrant_email = row[3]
                    if tut_id in tutorials:
                        tutorial = tutorials[tut_id]
                    else:
                        tutorial = PyConTutorialProposal.objects.get(proposalbase_ptr=tut_id)
                        if max_attendees:
                            tutorial.max_attendees = max_attendees
                        tutorial.save()
                        tutorials[tut_id] = tutorial
                    if tutorial in registrant_data:
                        registrant_data[tutorial].append(registrant_email)
                    else:
                        registrant_data[tutorial] = [registrant_email]

            # Add the Users objects to the associated Tutorial as registrants
            for tutorial, registrants in registrant_data.items():
                users = get_user_model().objects.filter(email__in=registrants)
                # Clear and update the registrants as these are essentially
                # Read only and updateable via CTE updates
                tutorial.registrants.clear()
                tutorial.registrants.add(*users)
                log.info("Updated %s registrant(s) for %s." % (users.count(), tutorial))
