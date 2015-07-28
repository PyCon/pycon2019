from pycon.finaid.utils import applications_open, has_application, is_reviewer


def financial_aid(request):
    open = applications_open()
    ctx = {
        "show_finaid_apply_button": open and not has_application(request.user),
        "show_finaid_edit_button": open and has_application(request.user),
        "show_finaid_status_button": has_application(request.user),
        "show_finaid_review_button": is_reviewer(request.user),
        "show_finaid_download_button": is_reviewer(request.user),
        #FIXME - figure out the requirements for when to show the finaid receipt form
        "show_finaid_receipt_form": has_application(request.user),
    }

    ctx["show_financial_aid_section"] = \
        ctx["show_finaid_apply_button"] or ctx["show_finaid_edit_button"] \
        or ctx["show_finaid_status_button"] or ctx["show_finaid_review_button"]

    return ctx
