from symposion.proposals.models import ProposalSection


def reviews(request):
    sections = []
    for section in ProposalSection.objects.select_related('section'):
        if request.user.has_perm("reviews.can_review_%s" % section.section.slug):
            sections.append(section)
    return {
        "review_sections": sections,
    }
