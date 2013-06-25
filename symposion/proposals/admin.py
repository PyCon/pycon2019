from django.contrib import admin

# from symposion.proposals.actions import export_as_csv_action
from symposion.proposals.models import ProposalSection, ProposalKind


# admin.site.register(Proposal,
#     list_display = [
#         "id",
#         "title",
#         "speaker",
#         "speaker_email",
#         "kind",
#         "audience_level",
#         "cancelled",
#     ],
#     list_filter = [
#         "kind__name",
#         "result__accepted",
#     ],
#     actions = [export_as_csv_action("CSV Export", fields=[
#         "id",
#         "title",
#         "speaker",
#         "speaker_email",
#         "kind",
#     ])]
# )

class ProposalSectionAdmin(admin.ModelAdmin):
    list_display = ['section', 'start', 'end', 'closed', 'published']


class ProposalKindAdmin(admin.ModelAdmin):
    list_display = ['section', 'name', 'slug']

admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalKind, ProposalKindAdmin)
