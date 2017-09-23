from django import forms

from django.core.exceptions import ValidationError
from django.template.defaultfilters import wordcount
from django.utils.translation import ugettext_lazy as _

from symposion.speakers.models import Speaker


class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = [
            "name",
            "biography",
            "photo",
            "twitter_username",
            "mobile_number",
            "interested_mentee",
            "interested_mentor",
            "financial_support",
        ]
        help_texts = {
            'mobile_number': _(
                u"For on-site use only,"
                u" in case we need to get in touch with you."
            ),
            'interested_mentee': _(
                u"We're trying something new this year... **tell people about "
                u"to expect if they check these boxes**"
            ),
            'interested_mentor': _(
                u"We're trying something new this year... **tell people about "
                u"to expect if they check these boxes**"
            ),
            'financial_support': _(
                u"PyCon does not want expenses to discourage you from "
                u"submitting a proposal, and offers financial support "
                u"with a preference for speakers. Check here to indicate "
                u"that you require assistance. This is not seen by the "
                u"proposal reviewers and does not affect the review of "
                u" your proposal."
            )
        }
        labels = {
            'interested_mentee': _(
                u"I'm interested in receiving mentorship in the following areas:"
            ),
            'interested_mentor': _(
                u"I'm interested in providing mentorship in the following ways:"
            ),
            'financial_support': _(
                u"I require financial assistance if my proposal is accepted."
            ),
        }

    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        if value.startswith("@"):
            value = value[1:]
        return value

    def clean_biography(self):
        value = self.cleaned_data["biography"]
        words = wordcount(value)
        if words > 100:
            raise ValidationError(_(u"Please limit speaker biography to 100 "
                                    u"words or less"))
        return value


# class SignupForm(PinaxSignupForm):

#     def save(self, speaker, request=None):
#         # don't assume a username is available. it is a common removal if
#         # site developer wants to use email authentication.
#         username = self.cleaned_data.get("username")
#         email = self.cleaned_data["email"]
#         new_user = self.create_user(username)
#         if speaker.invite_email == new_user.email:
#             # already verified so can just create
#             EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
#         else:
#             if request:
#                 messages.info(request, u"Confirmation email sent to %(email)s" % {"email": email})
#             EmailAddress.objects.add_email(new_user, email)
#             new_user.is_active = False
#             new_user.save()
#         self.after_signup(new_user)
#         return new_user
