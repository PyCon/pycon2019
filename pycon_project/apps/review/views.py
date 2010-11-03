from django.db.models import Q, Count
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from proposals.models import Proposal
from review.forms import ReviewForm, ReviewCommentForm, SpeakerCommentForm
from review.models import ReviewAssignment, Review, LatestVote, VOTES


def access_not_permitted(request):
    ctx = RequestContext(request)
    return render_to_response("reviews/access_not_permitted.html", ctx)


def proposals_generator(request, queryset, username=None, check_speaker=True):
    for obj in queryset:
        # @@@ this sucks; we can do better
        if check_speaker:
            if request.user in [s.user for s in obj.speakers()]:
                continue
        if obj.result is None:
            continue
        obj.comment_count = obj.result.comment_count
        obj.total_votes = obj.result.vote_count
        obj.plus_one = obj.result.plus_one
        obj.plus_zero = obj.result.plus_zero
        obj.minus_zero = obj.result.minus_zero
        obj.minus_one = obj.result.minus_one
        lookup_params = dict(proposal=obj)
        if username:
            lookup_params["user__username"] = username
        else:
            lookup_params["user"] = request.user
        try:
            obj.latest_vote = LatestVote.objects.get(**lookup_params).css_class()
        except LatestVote.DoesNotExist:
            obj.latest_vote = "no-vote"
        yield obj


def group_proposals(proposals):
    grouped = {}
    for proposal in proposals:
        session_type = proposal.session_type
        if session_type in grouped:
            grouped[session_type].append(proposal)
        else:
            grouped[session_type] = [proposal]
    return grouped


@login_required
def review_list(request, username=None):
    
    if username:
        # if they're not a reviewer admin and they aren't the person whose
        # review list is being asked for, don't let them in
        if not request.user.groups.filter(name="reviewers-admins").exists():
            if not request.user.username == username:
                return access_not_permitted(request)
    else:
        if not request.user.groups.filter(name="reviewers").exists():
            return access_not_permitted(request)
    
    queryset = Proposal.objects.select_related("speaker__user", "result")
    if username:
        reviewed = LatestVote.objects.filter(user__username=username).values_list("proposal", flat=True)
        queryset = queryset.filter(pk__in=reviewed)
    
    admin = request.user.groups.filter(name="reviewers-admins").exists()
    
    proposals = group_proposals(proposals_generator(request, queryset, username=username, check_speaker=not admin))
    
    ctx = {
        "proposals": proposals,
        "username": username,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("reviews/review_list.html", ctx)


@login_required
def review_admin(request):
    
    if not request.user.groups.filter(name="reviewers-admins").exists():
        return access_not_permitted(request)
    
    def reviewers():
        queryset = User.objects.distinct().filter(groups__name="reviewers")
        for obj in queryset:
            obj.comment_count = Review.objects.filter(user=obj).count()
            obj.total_votes = LatestVote.objects.filter(user=obj).count()
            obj.plus_one = LatestVote.objects.filter(
                user = obj,
                vote = LatestVote.VOTES.PLUS_ONE
            ).count()
            obj.plus_zero = LatestVote.objects.filter(
                user = obj,
                vote = LatestVote.VOTES.PLUS_ZERO
            ).count()
            obj.minus_zero = LatestVote.objects.filter(
                user = obj,
                vote = LatestVote.VOTES.MINUS_ZERO
            ).count()
            obj.minus_one = LatestVote.objects.filter(
                user = obj,
                vote = LatestVote.VOTES.MINUS_ONE
            ).count()
            yield obj
    ctx = {
        "reviewers": reviewers(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("reviews/review_admin.html", ctx)


@login_required
def review_detail(request, pk):
    proposals = Proposal.objects.select_related("result")
    proposal = get_object_or_404(proposals, pk=pk)
    
    admin = request.user.groups.filter(name="reviewers-admins").exists()
    speakers = [s.user for s in proposal.speakers()]
    
    if not request.user.groups.filter(name="reviewers").exists():
        return access_not_permitted(request)
    if not admin and request.user in speakers:
        return access_not_permitted(request)
    
    try:
        latest_vote = LatestVote.objects.get(proposal=proposal, user=request.user)
    except LatestVote.DoesNotExist:
        latest_vote = None
    
    if request.method == "POST":
        if request.user in speakers:
            return access_not_permitted(request)
        
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            
            review = review_form.save(commit=False)
            review.user = request.user
            review.proposal = proposal
            review.save()
            
            return redirect(request.path)
    else:
        initial = {}
        if latest_vote:
            initial["vote"] = latest_vote.vote
        review_form = ReviewForm(initial=initial)
    
    proposal.comment_count = proposal.result.comment_count
    proposal.total_votes = proposal.result.vote_count
    proposal.plus_one = proposal.result.plus_one
    proposal.plus_zero = proposal.result.plus_zero
    proposal.minus_zero = proposal.result.minus_zero
    proposal.minus_one = proposal.result.minus_one
    
    reviews = Review.objects.filter(proposal=proposal).order_by("-submitted_at")
    
    return render_to_response("reviews/review_detail.html", {
        "proposal": proposal,
        "latest_vote": latest_vote,
        "reviews": reviews,
        "review_form": review_form,
    }, context_instance=RequestContext(request))


@login_required
def review_stats(request):
    
    if not request.user.groups.filter(name="reviewers").exists():
        return access_not_permitted(request)
    
    proposals = Proposal.objects.select_related("speaker__user", "result")
    
    # proposals with at least one +1 and no -1s, sorted by the 'score'
    good = proposals.filter(result__plus_one__gt=0, result__minus_one=0).order_by("-result__score")
    # proposals with at least one -1 and no +1s, reverse sorted by the 'score'
    bad = proposals.filter(result__minus_one__gt=0, result__plus_one=0).order_by("result__score")
    # proposals with neither a +1 or a -1, sorted by total votes (lowest first)
    indifferent = proposals.filter(result__minus_one=0, result__plus_one=0).order_by("result__vote_count")
    # proposals with both a +1 and -1, sorted by total votes (highest first)
    controversial = proposals.filter(result__plus_one__gt=0, result__minus_one__gt=0).order_by("-result__vote_count")
    
    admin = request.user.groups.filter(name="reviewers-admins").exists()
    
    ctx = {
        "good_proposals": group_proposals(proposals_generator(request, good, check_speaker=not admin)),
        "bad_proposals": group_proposals(proposals_generator(request, bad, check_speaker=not admin)),
        "indifferent_proposals": group_proposals(proposals_generator(request, indifferent, check_speaker=not admin)),
        "controversial_proposals": group_proposals(proposals_generator(request, controversial, check_speaker=not admin)),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("reviews/review_stats.html", ctx)
