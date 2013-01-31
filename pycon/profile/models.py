from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.OneToOneField(User, related_name="profile")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    @property
    def is_complete(self):
        for key in self._meta.get_all_field_names():
            if key != "phone" and not getattr(self, key):
                return False
        return True
    
    @property
    def display_name(self):
        return " ".join([self.first_name, self.last_name])
