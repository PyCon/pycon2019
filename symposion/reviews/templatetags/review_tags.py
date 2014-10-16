import bleach

from django import template
from django.conf import settings

from symposion.reviews.models import Review, ReviewAssignment


register = template.Library()


@register.assignment_tag(takes_context=True)
def user_reviews(context):
    request = context["request"]
    reviews = Review.objects.filter(user=request.user)
    return reviews


@register.assignment_tag(takes_context=True)
def review_assignments(context):
    request = context["request"]
    assignments = ReviewAssignment.objects.filter(user=request.user)
    return assignments


@register.filter("bleach")
def _bleach(text):
    return bleach.clean(text, tags=settings.BLEACH_ALLOWED_TAGS)
