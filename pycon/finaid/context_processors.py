from pycon.finaid.utils import applications_open, has_application, is_reviewer


def financial_aid(request):

    ctx = {
        "financial_aid_open": applications_open(),
        "is_financial_aid_reviewer": is_reviewer(request.user),
        "has_applied_for_financial_aid": has_application(request.user),
    }
    ctx["show_financial_aid_section"] = \
        ctx['financial_aid_open'] \
        or ctx['is_financial_aid_reviewer'] \
        or ctx['has_applied_for_financial_aid']

    return ctx
