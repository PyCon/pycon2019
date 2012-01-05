from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from wakawaka.models import Revision, WikiPage

class WikiPageForm(forms.Form):
    content = forms.CharField(label=_('Content'), widget=forms.Textarea(attrs={'rows': 30}))
    message = forms.CharField(label=_('Change message (optional)'), widget=forms.TextInput, required=False)

    def save(self, request, page, *args, **kwargs):
        Revision.objects.create(
            page=page,
            creator=request.user,
            creator_ip=request.META['REMOTE_ADDR'],
            content = self.cleaned_data['content'],
            message = self.cleaned_data['message']
        )

DELETE_CHOICES = (

)

class DeleteWikiPageForm(forms.Form):
    delete = forms.ChoiceField(label=_('Delete'), choices=())

    def __init__(self, request, *args, **kwargs):
        '''
        Override the __init__ to display only delete choices the user has
        permission for.
        '''
        self.base_fields['delete'].choices = []
        if request.user.has_perm('wakawaka.delete_revision'):
            self.base_fields['delete'].choices.append(('rev', _('Delete this revision')),)

        if request.user.has_perm('wakawaka.delete_revision') and \
           request.user.has_perm('wakawaka.delete_wikipage'):
            self.base_fields['delete'].choices.append(('page', _('Delete the page with all revisions')),)

        super(DeleteWikiPageForm, self).__init__(*args, **kwargs)

    def _delete_page(self, page):
        page.delete()

    def _delete_revision(self, rev):
        rev.delete()

    def delete_wiki(self, request, page, rev):
        """
        Deletes the page with all revisions or the revision, based on the
        users choice.

        Returns a HttpResponseRedirect.
        """

        # Delete the page
        if self.cleaned_data.get('delete') == 'page' and \
           request.user.has_perm('wakawaka.delete_revision') and \
           request.user.has_perm('wakawaka.delete_wikipage'):
            self._delete_page(page)
            request.user.message_set.create(message=ugettext('The page %s was deleted' % page.slug))
            return HttpResponseRedirect(reverse('wakawaka_index'))

        # Revision handling
        if self.cleaned_data.get('delete') == 'rev':

            revision_length = len(page.revisions.all())

            # Delete the revision if there are more than 1 and the user has permission
            if revision_length > 1 and request.user.has_perm('wakawaka.delete_revision'):
                self._delete_revision(rev)
                request.user.message_set.create(message=ugettext('The revision for %s was deleted' % page.slug))
                return HttpResponseRedirect(reverse('wakawaka_page', kwargs={'slug': page.slug}))

            # Do not allow deleting the revision, if it's the only one and the user
            # has no permisson to delete the page.
            if revision_length <= 1 and \
               not request.user.has_perm('wakawaka.delete_wikipage'):
                request.user.message_set.create(message=ugettext('You can not delete this revison for %s because it\'s the only one and you have no permission to delete the whole page.' % page.slug))
                return HttpResponseRedirect(reverse('wakawaka_page', kwargs={'slug': page.slug}))

            # Delete the page and the revision if the user has both permissions
            if revision_length <= 1 and \
               request.user.has_perm('wakawaka.delete_revision') and \
               request.user.has_perm('wakawaka.delete_wikipage'):
                self._delete_page(page)
                request.user.message_set.create(message=ugettext('The page for %s was deleted because you deleted the only revision' % page.slug))
                return HttpResponseRedirect(reverse('wakawaka_index'))

        return None


