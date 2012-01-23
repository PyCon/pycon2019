from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from symposion.schedule.cache import db, cache_key, cache_key_user


class Command(BaseCommand):
    
    def delete(self, key):
        with db.lock("%s-lock" % key):
            db.delete(key)
    
    def handle(self, *args, **options):
        if db:
            self.delete(cache_key())
            for user in User.objects.all():
                self.delete(cache_key_user(user))