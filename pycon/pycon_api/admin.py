from django.contrib import admin
from pycon.pycon_api.models import APIAuth, ProposalData, IRCLogLine


class APIAuthAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')


class ProposalDataAdmin(admin.ModelAdmin):
    list_display = ('proposal',)


class IRCLogLineAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'timestamp', 'user', 'line')


admin.site.register(APIAuth, APIAuthAdmin)
admin.site.register(ProposalData, ProposalDataAdmin)
admin.site.register(IRCLogLine, IRCLogLineAdmin)
