from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from eldarion_test import TestCase

from sponsors.models import Sponsor, Benefit, SponsorLevel, BenefitLevel


class SponsorTests(TestCase):
    def setUp(self):
        self.linus = User.objects.create_user("linus", "linus@linux.org", "penguin")
        self.kant = User.objects.create_user("kant", "immanuel@kant.org", "justice")
    
    def test_index(self):
        response = self.get("sponsor_index")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up to be a sponsor")
        
        with self.login("linus", "penguin"):
            response = self.get("sponsor_index")
            self.assertContains(response, "Apply to be a sponsor")
            
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org"
            })
            self.assertEqual(response.status_code, 302)
            
            response = self.get("sponsor_index")
            self.assertContains(response, "Your sponsorship application is being processed.")
            
            s = Sponsor.objects.get()
            s.active = True
            s.save()
            
            response = self.get("sponsor_index")
            self.assertEqual(response.status_code, 302)
    
    def test_apply(self):
        response = self.get("sponsor_apply")
        self.assertEqual(response.status_code, 302)
        
        with self.login("linus", "penguin"):
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Sponsor.objects.count(), 0)

            response = self.get("sponsor_apply")
            self.assertEqual(response.status_code, 200)
            
            response = self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org",
            })
            self.assertEqual(response.status_code, 302)
            s = Sponsor.objects.get()
            self.assertEqual(s.applicant, self.linus)
            self.assertEqual(s.active, None)
            
            response = self.get("sponsor_apply")
            self.assertEqual(response.status_code, 302)
    
    def test_detail(self):
        with self.login("linus", "penguin"):
            self.post("sponsor_apply", data={
                "name": "Linux Foundation",
                "contact_name": "Linus Torvalds",
                "contact_email": "linus@linux.org",
            })
            s = Sponsor.objects.get()
            
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 302)

            s.active = True
            s.save()
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 200)
        
        with self.login("kant", "justice"):
            response = self.get("sponsor_detail", pk=s.pk)
            self.assertEqual(response.status_code, 302)
        
        response = self.get("sponsor_detail", pk=s.pk)
        self.assertEqual(response.status_code, 302)


class BenefitTests(TestCase):
    def setUp(self):
        self.linus = User.objects.create_user("linus", "linus@linux.org", "penguin")

        self.tin = SponsorLevel.objects.create(name='Tin', cost=10000, order=0)
        self.zinc = SponsorLevel.objects.create(name='Zinc', cost=5000, order=1)
        self.lead = SponsorLevel.objects.create(name='Lead', cost=2000, order=2)

        self.cookies = Benefit.objects.create(name='Cookies', type='simple')
        self.free_speech = Benefit.objects.create(name='Free Speech', type='text')

        BenefitLevel.objects.create(level=self.tin, benefit=self.cookies,
                                    other_limits='all you can eat')
        BenefitLevel.objects.create(level=self.tin, benefit=self.free_speech,
                                    max_words=100)
        BenefitLevel.objects.create(level=self.zinc, benefit=self.cookies,
                                    other_limits='only one')
        BenefitLevel.objects.create(level=self.lead, benefit=self.cookies,
                                    other_limits='crumbs')

    def check_benefits(self, sponsor, benefits):
        self.assertEqual([(unicode(b.benefit),
                           b.max_words, b.other_limits, b.active)
                          for b in sponsor.sponsor_benefits.all()],
                         benefits)
        
    def test_reset_benefits(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   level=self.zinc)
        self.check_benefits(s, [('Cookies', None, 'only one', True)])

        s.level = self.tin
        s.save()

        self.check_benefits(s, [('Cookies', None, 'all you can eat', True),
                                ('Free Speech', 100, '', True)])

        s.level = self.lead
        s.save()

        self.check_benefits(s, [('Cookies', None, 'crumbs', True),
                                ('Free Speech', None, '', False)])

        s.level = None
        s.save()
        
        self.check_benefits(s, [('Cookies', None, '', False),
                                ('Free Speech', None, '', False)])

    def test_enforce_max_words(self):
        s = Sponsor.objects.create(applicant=self.linus,
                                   name='Linux Foundation',
                                   contact_name='Linus Torvalds',
                                   contact_email='linus@linux.org',
                                   level=self.tin)

        sb = s.sponsor_benefits.get(benefit=self.free_speech)
        sb.text = 'FIRE! ' * 99
        sb.clean()
        sb.text = 'FIRE! ' * 101
        self.assertRaises(ValidationError, sb.clean)
