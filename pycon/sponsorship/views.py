from cStringIO import StringIO
import itertools
import logging
import os
import time
from zipfile import ZipFile, ZipInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from pycon.sponsorship.forms import SponsorApplicationForm, \
    SponsorBenefitsFormSet, SponsorDetailsForm
from pycon.sponsorship.models import Sponsor, SponsorBenefit


log = logging.getLogger(__name__)


@login_required
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = SponsorApplicationForm(user=request.user)
    
    return render_to_response("sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    
    if not sponsor.active or sponsor.applicant != request.user:
        return redirect("sponsor_list")
    
    formset_kwargs = {
        "instance": sponsor,
        "queryset": SponsorBenefit.objects.filter(active=True)
    }
    
    if request.method == "POST":
        
        form = SponsorDetailsForm(request.POST, instance=sponsor)
        formset = SponsorBenefitsFormSet(request.POST, request.FILES, **formset_kwargs)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, "Your sponsorship application has been submitted!")
            
            return redirect(request.path)
    else:
        form = SponsorDetailsForm(instance=sponsor)
        formset = SponsorBenefitsFormSet(**formset_kwargs)
    
    return render_to_response("sponsorship/detail.html", {
        "sponsor": sponsor,
        "form": form,
        "formset": formset,
    }, context_instance=RequestContext(request))


@staff_member_required
def sponsor_export_data(request):
    sponsors = []
    data = ""
    
    for sponsor in Sponsor.objects.order_by("added"):
        d = {
            "name": sponsor.name,
            "url": sponsor.external_url,
            "level": (sponsor.level.order, sponsor.level.name),
            "description": "",
        }
        for sponsor_benefit in sponsor.sponsor_benefits.all():
            if sponsor_benefit.benefit_id == 2:
                d["description"] = sponsor_benefit.text
        sponsors.append(d)
    
    def izip_longest(*args):
        fv = None
        def sentinel(counter=([fv]*(len(args)-1)).pop):
            yield counter()
        iters = [itertools.chain(it, sentinel(), itertools.repeat(fv)) for it in args]
        try:
            for tup in itertools.izip(*iters):
                yield tup
        except IndexError:
            pass
    def pairwise(iterable):
        a, b = itertools.tee(iterable)
        b.next()
        return izip_longest(a, b)
    
    def level_key(s):
        return s["level"]
    
    for level, level_sponsors in itertools.groupby(sorted(sponsors, key=level_key), level_key):
        data += "%s\n" % ("-" * (len(level[1])+4))
        data += "| %s |\n" % level[1]
        data += "%s\n\n" % ("-" * (len(level[1])+4))
        for sponsor, next in pairwise(level_sponsors):
            description = sponsor["description"].strip()
            description = description if description else "-- NO DESCRIPTION FOR THIS SPONSOR --"
            data += "%s\n\n%s" % (sponsor["name"], description)
            if next is not None:
                data += "\n\n%s\n\n" % ("-"*80)
            else:
                data += "\n\n"
    
    return HttpResponse(data, content_type="text/plain;charset=utf-8")


@staff_member_required
def sponsor_zip_logo_files(request):
    """Return a zip file of sponsor web and print logos"""

    zip_stringio = StringIO()
    with ZipFile(zip_stringio, "w") as zipfile:
        for benefit in SponsorBenefit.objects.filter(
                benefit__type__in=("file", "weblogo"))\
                .exclude(upload=''):
            if os.path.exists(benefit.upload.path):
                modtime = time.gmtime(os.stat(benefit.upload.path).st_mtime)
                with open(benefit.upload.path, "rb") as f:
                    zipinfo = ZipInfo(filename=benefit.upload.name,
                                      date_time=modtime)
                    zipfile.writestr(zipinfo, f.read())
            else:
                log.debug("No such sponsor file: %s" % benefit.upload.path)
    response = HttpResponse(zip_stringio.getvalue(),
                            content_type="application/zip")
    prefix = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]
    response['Content-Disposition'] = \
        'attachment; filename="pycon_%s_sponsorlogos.zip"' % prefix
    return response
