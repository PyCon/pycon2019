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
        logger.debug("Begin update tutorial registration numbers.")
        url = config.CTE_TUTORIAL_DATA_URL
        username = config.CTE_BASICAUTH_USER
        password = config.CTE_BASICAUTH_PASS
        if not all([url, username, password]):
            logger.warn("CTE tutorial registration may not be correctly configured.")
        auth = (username, password) if username and password else None
        response = requests.get(url, auth=auth)

        if not response.raise_for_status():
            User = get_user_model()
            tutorials = {}  # CTE ID: PyConTutorialProposal
            for row in csv.DictReader(response.content.splitlines()):
                if not row or not any(v.strip() for v in row.values()):
                    logger.debug("Skipping blank line.")
                    continue

                tut_id = row['tutorialnumber']
                tut_name = row['tutorialname']
                max_attendees = row['maxattendees']
                user_email = row['useremail']
                user_id = row['PyConID']

                if not tut_id:
                    logger.warn(
                        "Unable to register '{}' for '{}': Tutorial ID not "
                        "given.".format(user_email, tut_name))
                    continue

                if tut_id not in tutorials:
                    try:
                        # Try to get the tutorial by ID.
                        # If that fails, match name and set the tutorial
                        # ID on the found object.
                        tutorial = PyConTutorialProposal.objects.get(presentation=tut_id)
                    except PyConTutorialProposal.DoesNotExist:
                        logger.warn(
                            "Unable to register '{}[{}]' for '{}': Tutorial ID "
                            "{} is invalid.".format(user_email, user_id, tut_name, tut_id))
                        continue
                    except PyConTutorialProposal.MultipleObjectsReturned:
                        logger.warn(
                            "Unable to register '{}[{}] for '{}': Multiple "
                            "tutorials found for '{}' or '{}'".format(
                                user_email, user_id, tut_name, tut_name, tut_id))
                        continue
                    else:
                        # Clear the registrants as these are effectively
                        # read-only, and can only be updated via CTE.
                        tutorial.registrants.clear()
                        tutorial.registration_count = 0
                        tutorial.cte_tutorial_id = tut_id
                        tutorial.max_attendees = max_attendees or None
                        tutorials[tut_id] = tutorial
                tutorial = tutorials[tut_id]
                tutorial.registration_count += 1
                tutorial.save()

                try:
                    user = User.objects.get(id=int(user_id))
                except User.DoesNotExist:
                    logger.warn(
                        "Unable to register '{}[{}]' for '{}' ({}): User account "
                        "not found.".format(user_email, user_id, tut_name, tut_id))
                    continue
                except User.MultipleObjectsReturned:
                    logger.warn(
                        "Unable to register '{}[{}]' for '{}' ({}): "
                        "Multiple user accounts found for "
                        "email.".format(user_email, user_id, tut_name, tut_id))
                    continue
                else:
                    tutorial.registrants.add(user)
                    logger.debug(
                        "Successfully registered '{}[{}]' for '{}' "
                        "({}).".format(user_email, user_id, tut_name, tut_id))
        logger.debug("End update tutorial registration numbers.")
