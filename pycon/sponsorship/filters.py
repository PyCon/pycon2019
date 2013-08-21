# list filters for the admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from pycon.sponsorship.models import SponsorBenefit, BenefitLevel


class WebLogoFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'web logo'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'weblogo'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('complete', 'Complete'),
            ('incomplete', 'Incomplete'),
            ('na', 'N/A'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        complete_benefits = SponsorBenefit.objects.filter(benefit__name="Web logo", active=True, is_complete=True)
        incomplete_benefits = SponsorBenefit.objects.filter(benefit__name="Web logo", active=True, is_complete=False)
        if self.value() == 'complete':
            # has a web logo benefit and it is complete
            return queryset.filter(sponsor_benefits=complete_benefits)
        elif self.value() == 'incomplete':
            # has no web logo benefit, or it is incomplete
            has_benefit = Q(sponsor_benefits__benefit__name="Web logo")
            benefit_incomplete = Q(sponsor_benefits=incomplete_benefits)
            return queryset.filter(benefit_incomplete | ~has_benefit)
        elif self.value() == "na":
            # what levels are this benefit valid for?
            valid_levels = BenefitLevel.objects.filter(benefit__name="Web logo")
            return queryset.exclude(level__in=valid_levels)
