from django.contrib.auth.models import User

from eldarion_test import TestCase

from sponsors.models import Sponsor


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
