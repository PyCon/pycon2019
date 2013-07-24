from django.contrib import admin

from .models import FinancialAidApplication, FinancialAidMessage


admin.site.register(FinancialAidApplication)


def application__user(message):
    return message.application.user
application__user.short_description = u"Applicant"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'user', application__user)


admin.site.register(FinancialAidMessage, MessageAdmin)
