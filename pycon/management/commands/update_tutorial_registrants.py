import csv
import logging
import requests

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand

from constance import config

from pycon.models import PyConTutorialProposal


logger = logging.getLogger(__name__)


class Command(NoArgsCommand):
    """
    Parses an external CSV for tutorial registrant data and updates the
    corresponding Tutorial instance with registrant information.
    """

    def handle_noargs(self, **options):
        """Fetch the external URL and parse the data."""

        url = config.CTE_TUTORIAL_DATA_URL
        username = config.CTE_BASICAUTH_USER
        password = config.CTE_BASICAUTH_PASS
        auth = (username, password) if username and password else None
        response = requests.get(url, auth=auth)

        if not response.raise_for_status():
            User = get_user_model()
            tutorials = {}  # CTE ID: PyConTutorialProposal
            for row in csv.DictReader(response.content.splitlines()):
                if not row or not any(v.strip() for v in row.values()):
                    logger.info("Skipping blank line.")
                    continue

                tut_id = row['tutorialnumber']
                tut_name = row['tutorialname']
                max_attendees = row['maxattendees']
                user_email = row['useremail']

                if not tut_id:
                    logger.debug(
                        "Unable to register '{}' for '{}': Tutorial ID not "
                        "given.".format(user_email, tut_name))
                    continue

                if tut_id not in tutorials:
                    try:
                        tutorial = PyConTutorialProposal.objects.get(pk=tut_id)
                    except PyConTutorialProposal.DoesNotExist:
                        logger.debug(
                            "Unable to register '{}' for '{}': Tutorial ID "
                            "{} is invalid.".format(user_email, tut_name, tut_id))
                        continue
                    else:
                        # Clear the registrants as these are effectively
                        # read-only, and can only be updated via CTE.
                        tutorial.registrants.clear()
                        tutorial.max_attendees = max_attendees or None
                        tutorial.save()
                        tutorials[tut_id] = tutorial
                tutorial = tutorials[tut_id]

                try:
                    user = User.objects.get(email=user_email)
                except User.DoesNotExist:
                    logger.debug.write(
                        "Unable to register '{}' for '{}' ({}): User account "
                        "not found.".format(user_email, tut_name, tut_id))
                    continue
                else:
                    tutorial.registrants.add(user)
                    logger.info.write(
                        "Successfully registered '{}' for '{}' "
                        "({}).".format(user_email, tut_name, tut_id))
