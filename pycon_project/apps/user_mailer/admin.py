from django.contrib import admin

from user_mailer.models import EmailTemplate, Campaign


admin.site.register(EmailTemplate)
admin.site.register(Campaign)