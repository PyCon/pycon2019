from django.contrib import admin

from .models import FinancialAidApplication, FinancialAidApplicationPeriod,\
    FinancialAidMessage, FinancialAidEmailTemplate, Receipt


def application__user(obj):
    return obj.application.user
application__user.short_description = u"Applicant"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'user', application__user)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('timestamp', application__user, 'amount', 'receipt_image', )
    list_filter = ('application__user', )


admin.site.register(FinancialAidApplication)
admin.site.register(FinancialAidApplicationPeriod)
admin.site.register(FinancialAidMessage, MessageAdmin)
admin.site.register(FinancialAidEmailTemplate)
admin.site.register(Receipt, ReceiptAdmin)
