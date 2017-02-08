from django.db import models

class Registration(models.Model):
    class Meta:
        # Do not actually create a database table - this model exists
        # solely to create the permissions this module needs:
        managed = False

        permissions = (
            ('group_registration', 'Permission for a registrar to use the'
             ' registration/register/group/ form'),
        )
