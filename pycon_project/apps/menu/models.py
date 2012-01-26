from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class MenuItem(MPTTModel):
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children")
    url = models.CharField(max_length=200)
    published = models.BooleanField(default=True)
    login_required = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]
