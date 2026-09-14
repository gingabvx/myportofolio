from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Projects, Academic


class MainTest(TestCase):
    def setUp(self):
        self.projects = Projects.objects.create(
            title="MPK Trigarda Web Profile", 
            description="Creating a personal web profile for the MPK SMA Labsren organization.", 
            category="website"
        )
        self.academic = Academic.objects.create(
            institution="Universitas Indonesia",
            period="2025 - Present",
            description="Undergraduate Computer Science student.",
            order=1,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.projects.title)
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_project_model(self):
        self.assertEqual(str(self.projects), "MPK Trigarda Web Profile")
        self.assertEqual(self.projects.category, "website")
        self.assertTrue(self.projects.is_ongoing)

    def test_project_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.projects.title)
        self.assertContains(response, self.projects.description)
        self.assertContains(response, "Website")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}#profile"')

    def test_empty_project_page(self):
        Projects.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "No projects are currently available.")

    def test_completed_project(self):
        self.projects.ended_at = timezone.now()
        self.projects.save()
        response = self.client.get(reverse("main:show_projects"))

        self.assertFalse(self.projects.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

    def test_academic_url_is_accessible(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "academic.html")

    def test_academic_page(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.academic.institution)
        self.assertContains(response, self.academic.period)
        self.assertContains(response, self.academic.description)

    def test_empty_academic_page(self):
        Academic.objects.all().delete()
        response = self.client.get(reverse("main:show_academic"))

        self.assertContains(response, "No academic records are currently available.")
    