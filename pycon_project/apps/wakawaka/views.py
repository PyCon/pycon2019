import difflib
from datetime import datetime, timedelta

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User

from wakawaka.forms import WikiPageForm, DeleteWikiPageForm
from wakawaka.models import WikiPage, Revision
from wakawaka.settings import DEFAULT_INDEX, LOCK_CACHE_PREFIX, LOCK_TIMEOUT

__all__ = ['index', 'page', 'edit', 'revisions', 'changes', 'revision_list', 'page_list']

def index(request, template_name='wakawaka/page.html'):
    '''
    Redirects to the default wiki index name.
    '''
    kwargs = {
        'slug': DEFAULT_INDEX,
    }
    # be group aware
    group = getattr(request, "group", None)
    if group:
        redirect_to = request.bridge.reverse('wakawaka_page', group, kwargs=kwargs)
    else:
        redirect_to = reverse('wakawaka_page', kwargs=kwargs)
    return HttpResponseRedirect(redirect_to)

def page(request, slug, rev_id=None, template_name='wakawaka/page.html', extra_context=None):
    '''
    Displays a wiki page. Redirects to the edit view if the page doesn't exist.
    '''
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    try:
        if group:
            queryset = group.content_objects(WikiPage)
        else:
            queryset = WikiPage.objects.all()
        page = queryset.get(slug=slug)
        rev = page.current

        # Display an older revision if rev_id is given
        if rev_id:
            if group:
                revision_queryset = group.content_objects(Revision, join="page")
            else:
                revision_queryset = Revision.objects.all()
            rev_specific = revision_queryset.get(pk=rev_id)
            if rev.pk != rev_specific.pk:
                rev_specific.is_not_current = True
            rev = rev_specific

    # The Page does not exist, redirect to the edit form or
    # deny, if the user has no permission to add pages
    except WikiPage.DoesNotExist:
        if request.user.is_authenticated():
            kwargs = {
                'slug': slug,
            }
            if group:
                redirect_to = bridge.reverse('wakawaka_edit', group, kwargs=kwargs)
            else:
                redirect_to = reverse('wakawaka_edit', kwargs=kwargs)
            return HttpResponseRedirect(redirect_to)
        raise Http404
    template_context = {
        'page': page,
        'rev': rev,
        'group': group,
        'group_base': group_base,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))


def edit(request, slug, rev_id=None, template_name='wakawaka/edit.html',
         extra_context=None, wiki_page_form=WikiPageForm,
         wiki_delete_form=DeleteWikiPageForm):
    '''
    Displays the form for editing and deleting a page.
    '''
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    lock_owner = lock = None

    if request.user.is_authenticated():
        lock_id = request.user.id
    else:
        lock_id = request.session.session_key

    if group:
        lock_cache_key = "%s-lock-%s-%s" % (LOCK_CACHE_PREFIX, group.slug, slug)
    else:
        lock_cache_key = "%s-lock-%s" % (LOCK_CACHE_PREFIX, slug)

    cached = cache.get(lock_cache_key)
    if cached is not None:
        lock, lock_authorized, lock_timestamp = cached
    else:
        lock_authorized = request.user.is_authenticated()
        lock_timestamp = datetime.now()

    is_locked = lock is not None
    have_lock = lock == lock_id

    if lock_authorized and lock:
        lock_owner = User.objects.get(pk=lock)
    else:
        lock_owner = None

    # Get the page for slug and get a specific revision, if given
    try:
        if group:
            queryset = group.content_objects(WikiPage)
        else:
            queryset = WikiPage.objects.all()
        page = queryset.get(slug=slug)
        rev = page.current
        initial = {'content': page.current.content}
        has_permission = request.user.has_perms(('wakawaka.change_wikipage', 'wakawaka.change_revision'))

        # Do not allow editing wiki pages if the user has no permission
        # but special case any existing community/ slugs
        if not has_permission and not page.is_community:
            if have_lock:
                # Removing lock in case permissions were revoked or lock not removed before.
                cache.delete(lock_cache_key)
            return HttpResponseForbidden(ugettext('You don\'t have permission to edit pages.'))

        if rev_id:
            # There is a specific revision, fetch this
            rev_specific = Revision.objects.get(pk=rev_id)
            if rev.pk != rev_specific.pk:
                rev = rev_specific
                rev.is_not_current = True
                initial = {'content': rev.content, 'message': _('Reverted to "%s"' % rev.message)}


    # This page does not exist, create a dummy page
    # Note that it's not saved here
    except WikiPage.DoesNotExist:

        # Do not allow adding wiki pages if the user has no permission
        if not request.user.has_perms(('wakawaka.add_wikipage', 'wakawaka.add_revision',)):
            return HttpResponseForbidden(ugettext('You don\'t have permission to add wiki pages.'))

        page = WikiPage(slug=slug)
        page.is_initial = True
        rev = None
        initial = {'content': _('Describe your new page %s here...' % slug),
                   'message': _('Initial revision')}

    # Creating/canceling/resetting the lock
    cancel_lock = have_lock and request.GET.get('cancel_lock')
    if is_locked and cancel_lock:
        cache.delete(lock_cache_key)
        return HttpResponseRedirect(page.get_absolute_url())

    allowed_to_reset = request.user.has_perm('wakawaka.reset_lock')
    reset_lock = allowed_to_reset and request.GET.get('reset_lock')
    if not is_locked or reset_lock:
        cache.set(lock_cache_key, (lock_id, lock_authorized, datetime.now()), LOCK_TIMEOUT)
        if reset_lock:
            return HttpResponseRedirect(".")
        is_locked = have_lock = True

    # Don't display the delete form if the user has nor permission
    delete_form = None
    # The user has permission, then do
    if request.user.has_perm('wakawaka.delete_wikipage') or \
       request.user.has_perm('wakawaka.delete_revision'):
        delete_form = wiki_delete_form(request)
        if request.method == 'POST' and request.POST.get('delete'):
            delete_form = wiki_delete_form(request, request.POST)
            if delete_form.is_valid():
                return delete_form.delete_wiki(request, page, rev)

    # Page add/edit form
    form = wiki_page_form(initial=initial)
    if request.method == 'POST':
        form = wiki_page_form(data=request.POST)
        if form.is_valid():
            # Check if the content is changed, except there is a rev_id and the
            # user possibly only reverted the HEAD to it
            if not rev_id and initial['content'] == form.cleaned_data['content']:
                form.errors['content'] = (_('You have made no changes!'),)

            # Save the form and redirect to the page view
            else:
                try:
                    # Check that the page already exist
                    if group:
                        queryset = group.content_objects(WikiPage)
                    else:
                        queryset = WikiPage.objects.all()
                    page = queryset.get(slug=slug)
                except WikiPage.DoesNotExist:
                    # Must be a new one, create that page
                    page = WikiPage(slug=slug)
                    if group:
                        page = group.associate(page, commit=False)
                    page.save()

                form.save(request, page)

                if have_lock:
                    # Removing lock in case permissions were revoked or lock not removed before.
                    cache.delete(lock_cache_key)
                
                kwargs = {
                    'slug': page.slug,
                }
                
                if group:
                    redirect_to = bridge.reverse('wakawaka_page', group, kwargs=kwargs)
                else:
                    redirect_to = reverse('wakawaka_page', kwargs=kwargs)
                
                request.user.message_set.create(message=ugettext('Your changes to %s were saved' % page.slug))
                return HttpResponseRedirect(redirect_to)

    template_context = {
        'form': form,
        'delete_form': delete_form,
        'page': page,
        'rev': rev,
        'group': group,
        'group_base': group_base,
        'is_locked': is_locked,
        'have_lock': have_lock,
        'lock_owner': lock_owner,
        'lock_authorized': lock_authorized,
        'lock_timestamp': lock_timestamp,
        'lock_ttl': lock_timestamp + timedelta(seconds=LOCK_TIMEOUT),
        'allowed_to_reset': allowed_to_reset,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

def revisions(request, slug, template_name='wakawaka/revisions.html', extra_context=None):
    '''
    Displays the list of all revisions for a specific WikiPage
    '''
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    if group:
        queryset = group.content_objects(WikiPage)
    else:
        queryset = WikiPage.objects.all()
    page = get_object_or_404(queryset, slug=slug)

    template_context = {
        'page': page,
        'group': group,
        'group_base': group_base,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

def changes(request, slug, template_name='wakawaka/changes.html', extra_context=None):
    '''
    Displays the changes between two revisions.
    '''
    
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    rev_a_id = request.GET.get('a', None)
    rev_b_id = request.GET.get('b', None)

    # Some stinky fingers manipulated the url
    if not rev_a_id or not rev_b_id:
        return HttpResponseBadRequest('Bad Request')

    try:
        if group:
            revision_queryset = group.content_objects(Revision, join="page")
            wikipage_queryset = group.content_objects(WikiPage)
        else:
            revision_queryset = Revision.objects.all()
            wikipage_queryset = WikiPage.objects.all()
        rev_a = revision_queryset.get(pk=rev_a_id)
        rev_b = revision_queryset.get(pk=rev_b_id)
        page = wikipage_queryset.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    if rev_a.content != rev_b.content:
        d = difflib.unified_diff(rev_b.content.splitlines(),
                                 rev_a.content.splitlines(),
                                 'Original', 'Current', lineterm='')
        difftext = '\n'.join(d)
    else:
        difftext = _(u'No changes were made between this two files.')

    template_context = {
        'page': page,
        'diff': difftext,
        'rev_a': rev_a,
        'rev_b': rev_b,
        'group': group,
        'group_base': group_base,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

# Some useful views
def revision_list(request, template_name='wakawaka/revision_list.html', extra_context=None):
    '''
    Displays a list of all recent revisions.
    '''
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    if group:
        revision_list = group.content_objects(Revision, join="page")
    else:
        revision_list = Revision.objects.all()

    template_context = {
        'revision_list': revision_list,
        'group': group,
        'group_base': group_base,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

def page_list(request, template_name='wakawaka/page_list.html', extra_context=None):
    '''
    Displays all Pages
    '''
    if extra_context is None:
        extra_context = {}

    # be group aware
    group = getattr(request, "group", None)
    if group:
        bridge = request.bridge
        group_base = bridge.group_base_template()
    else:
        bridge = None
        group_base = None

    if group:
        page_list = group.content_objects(WikiPage)
    else:
        page_list = WikiPage.objects.all()
    page_list = page_list.order_by('slug')

    template_context = {
        'page_list': page_list,
        'index_slug': DEFAULT_INDEX,
        'group': group,
        'group_base': group_base,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))