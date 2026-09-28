from django.contrib.auth.models import Group, User
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
        self.projects.status = "completed"
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
    


class EditorRoleTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.academic = Academic.objects.create(
            institution="Universitas Indonesia", period="2025 - Now", description="Ilmu Komputer"
        )
        cls.project = Projects.objects.create(title="Portofolio", description="Web portofolio")
        cls.regular = User.objects.create_user("regular", password="pw12345!")
        cls.editor = User.objects.create_user("editor", password="pw12345!")
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.owner = User.objects.create_superuser("owner", password="pw12345!")

    def urls(self):
        return {
            "academic_create": reverse("main:create_academic"),
            "academic_edit": reverse("main:edit_academic", args=[self.academic.id]),
            "academic_delete": reverse("main:delete_academic", args=[self.academic.id]),
            "project_create": reverse("main:create_project"),
            "project_edit": reverse("main:edit_project", args=[self.project.id]),
            "project_delete": reverse("main:delete_project", args=[self.project.id]),
        }

    def test_visitor_redirected_to_login(self):
        for url in self.urls().values():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, url)
            self.assertTrue(response.url.startswith("/login/"), url)

    def test_regular_user_forbidden(self):
        self.client.force_login(self.regular)
        for url in self.urls().values():
            self.assertEqual(self.client.get(url).status_code, 403, url)
            self.assertEqual(self.client.post(url, {}).status_code, 403, url)

    def test_editor_can_edit_but_not_create_or_delete(self):
        self.client.force_login(self.editor)
        urls = self.urls()
        self.assertEqual(self.client.get(urls["academic_edit"]).status_code, 200)
        self.assertEqual(self.client.get(urls["project_edit"]).status_code, 200)
        for key in ("academic_create", "academic_delete", "project_create", "project_delete"):
            self.assertEqual(self.client.post(urls[key], {}).status_code, 403, key)
        self.assertTrue(Academic.objects.filter(pk=self.academic.pk).exists())
        self.assertTrue(Projects.objects.filter(pk=self.project.pk).exists())

    def test_editor_edit_saves_changes(self):
        self.client.force_login(self.editor)
        self.client.post(
            reverse("main:edit_academic", args=[self.academic.id]),
            {"institution": "UI Depok", "period": "2025", "description": "baru", "order": 1},
        )
        self.academic.refresh_from_db()
        self.assertEqual(self.academic.institution, "UI Depok")
        self.client.post(
            reverse("main:edit_project", args=[self.project.id]),
            {"title": "Portofolio v2", "description": "baru", "category": "website", "status": "completed"},
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portofolio v2")

    def test_buttons_per_role(self):
        edit = reverse("main:edit_academic", args=[self.academic.id])
        add = reverse("main:create_academic")
        delete = reverse("main:delete_academic", args=[self.academic.id])

        html = self.client.get(reverse("main:show_academic")).content.decode()
        for url in (edit, add, delete):
            self.assertNotIn(url, html)

        self.client.force_login(self.regular)
        html = self.client.get(reverse("main:show_academic")).content.decode()
        for url in (edit, add, delete):
            self.assertNotIn(url, html)

        self.client.force_login(self.editor)
        html = self.client.get(reverse("main:show_academic")).content.decode()
        self.assertIn(edit, html)
        self.assertNotIn(add, html)
        self.assertNotIn(delete, html)

        self.client.force_login(self.owner)
        html = self.client.get(reverse("main:show_academic")).content.decode()
        for url in (edit, add, delete):
            self.assertIn(url, html)

    def test_superuser_full_access(self):
        self.client.force_login(self.owner)
        urls = self.urls()
        self.client.post(urls["academic_delete"])
        self.client.post(urls["project_delete"])
        self.assertFalse(Academic.objects.exists())
        self.assertFalse(Projects.objects.exists())
