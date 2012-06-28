from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from account.mixins import LoginRequiredMixin
from social_auth.decorators import dsa_view
from social_auth.models import UserSocialAuth
from social_auth.utils import backend_setting
from social_auth.views import DEFAULT_REDIRECT


class SocialAuths(LoginRequiredMixin, ListView):

    model = UserSocialAuth

    def get_queryset(self):
        qs = super(SocialAuths, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


@login_required
@dsa_view()
def disconnect(request, backend, association_id=None):
    associated = request.user.social_auth.count()
    url = request.REQUEST.get(REDIRECT_FIELD_NAME, '') or backend_setting(backend, 'SOCIAL_AUTH_DISCONNECT_REDIRECT_URL') or DEFAULT_REDIRECT

    if not request.user.has_usable_password() and associated <= 1:
        messages.error(request, _("Cannot remove the only Social Account without first setting a Password or adding another Social Account."))
        return HttpResponseRedirect(url)

    usa = request.user.social_auth.get(pk=association_id)

    backend.disconnect(request.user, association_id)
    messages.success(request, _("Removed the %(provider)s account '%(uid)s'.") % {
        "provider": usa.provider,
        "uid": usa.extra_data.get("display", usa.uid) if usa.extra_data is not None else usa.uid,
    })

    return HttpResponseRedirect(url)
