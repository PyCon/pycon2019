from django.contrib import admin

from sponsors.models import SponsorLevel, Sponsor, SponsorLogo


class SponsorLogoInline(admin.StackedInline):
    model = SponsorLogo
    extra = 1


class SponsorAdmin(admin.ModelAdmin):
    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields['active'].widget.choices = [(u'1', "unreviewed"),
                                                     (u'2', "approved"),
                                                     (u'3', "rejected")]
        return form
    
    inlines = [SponsorLogoInline]
    
admin.site.register(SponsorLevel)
admin.site.register(Sponsor, SponsorAdmin)
