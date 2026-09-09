from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Projects


class MainTest(TestCase):
    def setUp(self):
        self.projects = Projects.objects.create(
            title="MPK Trigarda Web Profile", 
            description="Creating a personal web profile for the MPK SMA Labsren organization.", 
            category="website"
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
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}#profile"')

    def test_empty_project_page(self):
        Projects.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada projek yang ditambahkan.")

    def test_completed_project(self):
        self.projects.ended_at = timezone.now()
        self.projects.save()
        response = self.client.get(reverse("main:show_projects"))

        self.assertFalse(self.projects.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")