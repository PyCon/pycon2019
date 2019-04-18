from pycon.finaid.utils import applications_open, has_application, is_reviewer,\
    offer_accepted, has_withdrawn_application


def financial_aid(request):
    open = applications_open()
    if has_application(request.user):
        application = request.user.financial_aid
    else:
        application = None

    ctx = {
        "show_finaid_apply_button": open and (not application or has_withdrawn_application(request.user)),
        "show_finaid_edit_button": application and application.show_edit_button,
        "show_finaid_status_button": application and application.show_status_button,
        "show_finaid_review_button": is_reviewer(request.user),
        "show_finaid_receipt_review_button": is_reviewer(request.user) and request.user.has_perm('finaid.can_review_receipts'),
        "show_finaid_download_button": is_reviewer(request.user),
        "show_finaid_receipt_form": offer_accepted(request.user),
        "show_finaid_withdraw_button": application and application.show_withdraw_button,
        "show_finaid_accept_button": application and application.show_accept_button,
        "show_finaid_decline_button": application and application.show_decline_button,
        "show_finaid_request_more_button": application and application.show_request_more_button,
        "show_finaid_provide_info_button": application and application.show_provide_info_button,
        "show_finaid_reimbursement_update": application and application.review and application.review.amount > 0,
    }

    ctx["show_financial_aid_section"] = \
        ctx["show_finaid_apply_button"] or ctx["show_finaid_edit_button"] \
        or ctx["show_finaid_status_button"] or ctx["show_finaid_review_button"]

    return ctx
