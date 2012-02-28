def migrate():
    from symposion.schedule.models import Presentation
    for p in Presentation.objects.all():
        if p.kind.name == "Tutorial":
            p.released = False
        else:
            p.released = True
        p.save()