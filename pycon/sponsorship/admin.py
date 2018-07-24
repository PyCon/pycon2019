from urllib import quote

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from pycon.sponsorship.models import SponsorLevel, SponsorPackage, Sponsor, Benefit, \
    BenefitLevel, BenefitPackage, SponsorBenefit, BENEFITS
from pycon.sponsorship.views import email_selected_sponsors_action


class BenefitLevelInline(admin.TabularInline):
    model = BenefitLevel
    extra = 0


class BenefitPackageInline(admin.TabularInline):
    model = BenefitPackage
    extra = 0


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0
    fieldsets = [
        (None, {
            "fields": [
                ("benefit", "active"),
                ("max_words", "other_limits"),
                "text",
                "upload",
            ]
        })
    ]


class SponsorAdmin(admin.ModelAdmin):
    save_on_top = True
    actions = [email_selected_sponsors_action]
    list_per_page = 1000000  # Do not limit sponsors per page, just one big page
    fieldsets = [
        (None, {
            "fields": ["name", "applicant", "level", "packages", "external_url",
                       "display_url", "twitter_username", "annotation",
                       "web_description", "web_logo",
                       ("active", "approval_time")],
        }),
        ("Desired benefits", {
            "fields": ["wants_table", "wants_booth", "small_entity_discount"],
        }),
        ("Sponsor Data", {
            "fields": ["booth_number", "job_fair_participant",
                       "job_fair_table_number", "registration_promo_codes",
                       "expo_promo_codes"],
        }),
        ("Contact Information", {
            "fields": ["contact_name", "contact_emails", "contact_phone",
                       "contact_address"],
        }),
        ("Metadata", {
            "fields": ["added"],
            "classes": ["collapse"],
        })
    ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }
    inlines = [SponsorBenefitInline]
    # NB: We add to list_display and list_filter below
    list_display = ["name", "level", "contact", "applicant_field", "active",
                    "approval_time"]
    list_filter = ["level", "active"]
    readonly_fields = ["approval_time"]

    def contact(self, sponsor):
        # comma-separated emails in mailto: should work: https://www.ietf.org/rfc/rfc2368.txt
        # but the commas need to be URL-quoted
        return format_html(
            u'<a href="mailto:{}">{}</a>',
            quote(u','.join(sponsor.contact_emails)),
            sponsor.contact_name
        )

    def applicant_field(self, sponsor):
        name = sponsor.applicant.get_full_name()
        email = sponsor.applicant.email
        return mark_safe('<a href="mailto:%s">%s</a>' % (escape(email), escape(name)))
    applicant_field.short_description = _(u"Applicant")

    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)

        form.base_fields["active"].widget.choices = [
            (u"1", _(u"unreviewed")),
            (u"2", _(u"approved")),
            (u"3", _(u"rejected"))
        ]

        applicant_qs = form.base_fields['applicant'].queryset
        applicant_qs = applicant_qs.order_by('first_name', 'last_name', 'pk')
        form.base_fields['applicant'].queryset = applicant_qs

        return form

    # Define accessor functions for our benefit fields and add them to
    # list_display, so we can sort on them and give them sensible names.
    # Add the fields to list_filters while we're at it.
    for benefit in BENEFITS:
        benefit_name = benefit['name']
        field_name = benefit['field_name']

        def func_generator(ben):
            def column_func(obj):
                return getattr(obj, ben['field_name'])
            column_func.short_description = ben['column_title']
            column_func.boolean = True
            column_func.admin_order_field = ben['field_name']
            return column_func
        list_display.append(func_generator(benefit))
        list_filter.append(field_name)

    def save_related(self, request, form, formsets, change):
        super(SponsorAdmin, self).save_related(request, form, formsets, change)
        obj = form.instance
        obj.save()


class BenefitAdmin(admin.ModelAdmin):
    inlines = [BenefitLevelInline, BenefitPackageInline]
    list_display = ['name', 'type', 'levels', 'packages']
    list_filter = ['benefit_levels__level', 'benefit_packages__package']

    def levels(self, benefit):
        return u", ".join(l.level.name for l in benefit.benefit_levels.all())

    def packages(self, benefit):
        return u", ".join(p.package.name for p in benefit.benefit_packages.all())


class SponsorLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'order', 'cost', 'benefits']
    list_editable = ['order']
    list_filter = ['conference', 'benefit_levels__benefit']
    inlines = [BenefitLevelInline]

    def benefits(self, obj):
        return ', '.join(obj.benefit_levels.values_list('benefit__name', flat=True))


class SponsorPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'available', 'order', 'cost', 'benefits']
    list_editable = ['order']
    list_filter = ['conference', 'benefit_packages__benefit']
    inlines = [BenefitPackageInline]

    def benefits(self, obj):
        return ', '.join(obj.benefit_packages.values_list('benefit__name', flat=True))


admin.site.register(SponsorLevel, SponsorLevelAdmin)
admin.site.register(SponsorPackage, SponsorPackageAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(SponsorBenefit,
                    list_display=('benefit', 'sponsor', 'active', '_is_complete'))
