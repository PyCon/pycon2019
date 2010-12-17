import datetime

from django.conf import settings
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from mailer import send_mass_mail

from user_mailer.forms import CampaignCreateForm
from user_mailer.models import Campaign, EmailTemplate


@staff_member_required
def campaign_create(request):
    if request.method == "POST":
        form = CampaignCreateForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            return redirect("campaign_review", campaign.pk)
    else:
        form = CampaignCreateForm(initial={"from_address": request.user.email})
    ctx = {
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("user_mailer/campaign_create.html", ctx)


@staff_member_required
def campaign_review(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    ctx = {
        "campaign": campaign,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("user_mailer/campaign_review.html", ctx)


@staff_member_required
def campaign_submit(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    campaigns = Campaign.objects.select_related("email_template")
    campaign = get_object_or_404(campaigns, pk=pk)
    messages = []
    for user in campaign:
        email_ctx = {
            "user": user,
        }
        messages.append((
            campaign.email_template.render_subject(email_ctx),
            campaign.email_template.render_body(email_ctx),
            campaign.from_address,
            [user.email],
        ))
    send_mass_mail(messages)
    campaign.sent = datetime.datetime.now()
    campaign.save()
    return redirect("campaign_review", campaign.pk)


def campaign_email_preview(request, pk, to_user_pk=None):
    campaigns = Campaign.objects.select_related("email_template")
    campaign = get_object_or_404(campaigns, pk=pk)
    email_ctx = {}
    if to_user_pk:
        try:
            to_user = dict([(u.pk, u) for u in campaign])[int(to_user_pk)]
            email_ctx["user"] = to_user
        except KeyError:
            raise Http404("User not found in campaign")
    ctx = {
        "campaign": campaign,
        "subject": campaign.email_template.render_subject(email_ctx),
        "to_user": to_user,
        "from_address": campaign.from_address,
        "body": campaign.email_template.render_body(email_ctx),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("user_mailer/campaign_email_preview.html", ctx)
