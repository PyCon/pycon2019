def migrate():
    from symposion.reviews.models import ProposalResult
    for result in ProposalResult.objects.all():
        if result.accepted is True:
            result.status = "accepted"
        elif result.accepted is False:
            result.status = "rejected"
        elif result.accepted is None:
            result.status = "undecided"
        result.save()
