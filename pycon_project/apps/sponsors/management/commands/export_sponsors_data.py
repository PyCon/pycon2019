import csv
import zipfile

from django.core.management.base import BaseCommand, CommandError

from sponsors.models import Sponsor


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for sponsor in Sponsor.objects.all():
            data = {
                "name": sponsor.name,
                "url": sponsor.external_url,
                "description": "",
            }
            for sponsor_benefit in sponsor.sponsor_benefits.all():
                if sponsor_benefit.benefit_id == 2:
                    data["description"] = sponsor_benefit.text
                if sponsor_benefit.benefit_id == 1:
                    if sponsor_benefit.upload:
                        data["ad"] = sponsor_benefit.upload.path
                if sponsor_benefit.benefit_id == 7:
                    if sponsor_benefit.upload:
                        data["logo"] = sponsor_benefit.upload.path
            if "ad" in data:
                ad_path = data.pop("ad")
                # write to build directory
            if "logo" in data:
                logo_path = data.pop("logo")
                # write to build directory
            # write data to csv in build dir
            # zip build directory