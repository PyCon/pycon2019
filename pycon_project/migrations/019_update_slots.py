def migrate():
    from django.contrib.contenttypes.models import ContentType
    from symposion.schedule.models import Presentation
    ct = ContentType.objects.get_for_model(Presentation)
    for p in Presentation.objects.filter(slot__isnull=False, kind__name="Tutorial"):
        s = p.slot
        s.kind = ct
        s.save()
