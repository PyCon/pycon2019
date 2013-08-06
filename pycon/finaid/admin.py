from django.contrib import admin

from .models import FinancialAidApplication, FinancialAidApplicationPeriod,\
    FinancialAidMessage, FinancialAidEmailTemplate


def application__user(message):
    return message.application.user
application__user.short_description = u"Applicant"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'user', application__user)


admin.site.register(FinancialAidApplication)
admin.site.register(FinancialAidApplicationPeriod)
admin.site.register(FinancialAidMessage, MessageAdmin)
admin.site.register(FinancialAidEmailTemplate)
