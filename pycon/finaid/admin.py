from django.contrib import admin

from .models import FinancialAidApplication, FinancialAidApplicationPeriod,\
    FinancialAidMessage, FinancialAidEmailTemplate, Receipt


def application__user(obj):
    return obj.application.user
application__user.short_description = u"Applicant"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'user', application__user)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('timestamp', application__user, 'amount', 'receipt_image', 'approved', 'flagged', 'logged')
    list_filter = ('logged', 'approved', 'flagged', )
    search_fields = ('application__user__first_name', 'application__user__last_name', 'application__user__email')
    readonly_fields = ('approved_by', 'flagged_by')


def user(obj):
    return obj.user

class ApplicationAdmin(admin.ModelAdmin):
    list_display = (user, 'application_type', 'get_status_display')
    list_filter = ('application_type',)
    search_fields = ('user__first_name', 'user__last_name', 'application_type')
    readonly_fields = ('legal_name', 'address', 'disbursment_details')

admin.site.register(FinancialAidApplication, ApplicationAdmin)
admin.site.register(FinancialAidApplicationPeriod)
admin.site.register(FinancialAidMessage, MessageAdmin)
admin.site.register(FinancialAidEmailTemplate)
admin.site.register(Receipt, ReceiptAdmin)
