import datetime

from django.core import serializers
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class ObjectLog(models.Model):
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    user = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    raw_data = models.TextField()
    
    @classmethod
    def log(cls, instance, user=None):
        content_type = ContentType.objects.get_for_model(instance)
        queryset = content_type.model_class()._default_manager.filter(pk=instance.pk)
        raw_data = serializers.serialize("json", queryset, use_natural_keys=True)
        cls.objects.create(
            content_type = content_type,
            object_id = instance.id,
            user = user,
            raw_data = raw_data,
        )