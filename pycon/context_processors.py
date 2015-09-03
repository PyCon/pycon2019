from django.conf import settings


def global_settings(request):
    return {
        'CONFERENCE_YEAR': settings.CONFERENCE_YEAR,
        'REGISTRATION_EMAIL': settings.REGISTRATION_EMAIL,
    }
