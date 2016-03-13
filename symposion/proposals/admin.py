from django.contrib import admin
from django.contrib.auth.models import Permission

# from symposion.proposals.actions import export_as_csv_action
from symposion.proposals import models


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

admin.site.register(models.ProposalSection, ProposalSectionAdmin)
admin.site.register(models.ProposalKind, ProposalKindAdmin)
admin.site.register(models.AdditionalSpeaker)
admin.site.register(Permission,
                    list_display=['content_type', 'codename', 'name'],
                    search_fields=['codename', 'name'])
