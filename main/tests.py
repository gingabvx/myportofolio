from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
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
        for element_id in ("loading", "error", "empty", "grid"):
            self.assertContains(response, f'id="{element_id}"')
        self.assertContains(response, f'href="{reverse("main:show_main")}#profile"')

    def test_projects_json(self):
        fields = self.client.get(reverse("main:get_projects_json")).json()[0]["fields"]

        self.assertEqual(fields["title"], self.projects.title)
        self.assertEqual(fields["description"], self.projects.description)
        self.assertEqual(fields["category_display"], "Website")
        self.assertEqual(fields["status_display"], "Ongoing")

    def test_empty_projects_json(self):
        Projects.objects.all().delete()

        self.assertEqual(self.client.get(reverse("main:get_projects_json")).json(), [])

    def test_completed_project(self):
        self.projects.status = "completed"
        self.projects.save()
        fields = self.client.get(reverse("main:get_projects_json")).json()[0]["fields"]

        self.assertFalse(self.projects.is_ongoing)
        self.assertEqual(fields["status_display"], "Completed")

    def test_academic_url_is_accessible(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "academic.html")

    def test_academic_page_renders_skeleton_only(self):
        response = self.client.get(reverse("main:show_academic"))

        self.assertEqual(response.status_code, 200)
        for element_id in ("loading", "error", "empty", "grid"):
            self.assertContains(response, f'id="{element_id}"')
        # Data tidak lagi dirender server; JavaScript mengambilnya dari endpoint JSON.
        self.assertNotContains(response, self.academic.description)
        self.assertContains(response, reverse("main:get_academics_json"))

    def test_academic_json(self):
        response = self.client.get(reverse("main:get_academics_json"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(data[0]["pk"], str(self.academic.id))
        self.assertEqual(fields["institution"], self.academic.institution)
        self.assertEqual(fields["period"], self.academic.period)
        self.assertEqual(fields["description"], self.academic.description)
        self.assertEqual(fields["star_count"], 0)
        self.assertFalse(fields["is_starred"])

    def test_academic_json_search(self):
        Academic.objects.create(institution="SMA Contoh", period="2022", description="x")

        response = self.client.get(reverse("main:get_academics_json"), {"q": "contoh"})
        self.assertEqual([i["fields"]["institution"] for i in response.json()], ["SMA Contoh"])

        response = self.client.get(reverse("main:get_academics_json"), {"q": "tidak ada"})
        self.assertEqual(response.json(), [])

    def test_academic_json_star_info_for_logged_in_user(self):
        user = User.objects.create_user("starrer", password="pw12345!")
        self.academic.starred_by.add(user)

        fields = self.client.get(reverse("main:get_academics_json")).json()[0]["fields"]
        self.assertEqual(fields["star_count"], 1)
        self.assertFalse(fields["is_starred"])
        self.assertEqual(fields["starred_by_names"], "starrer")

        self.client.force_login(user)
        fields = self.client.get(reverse("main:get_academics_json")).json()[0]["fields"]
        self.assertTrue(fields["is_starred"])

    def test_empty_academic_json(self):
        Academic.objects.all().delete()
        response = self.client.get(reverse("main:get_academics_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


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

    def test_role_flags_per_role(self):
        add = 'popovertarget="add-academic-modal"'

        def flags(user=None):
            if user:
                self.client.force_login(user)
            html = self.client.get(reverse("main:show_academic")).content.decode()
            return (
                'const CAN_EDIT = "true" === "true"' in html,
                'const IS_SUPERUSER = "true" === "true"' in html,
                add in html,
            )

        # (bisa edit, superuser, tombol tambah)
        self.assertEqual(flags(), (False, False, False))
        self.assertEqual(flags(self.regular), (False, False, False))
        self.assertEqual(flags(self.editor), (True, False, False))
        self.assertEqual(flags(self.owner), (True, True, True))

    def test_superuser_full_access(self):
        self.client.force_login(self.owner)
        urls = self.urls()
        self.client.post(urls["academic_delete"])
        self.client.post(urls["project_delete"])
        self.assertFalse(Academic.objects.exists())
        self.assertFalse(Projects.objects.exists())


class AcademicCreateAjaxTests(TestCase):
    VALID = {"institution": "SMA Baru", "period": "2022 - 2025", "description": "Jurusan IPA", "order": 5}

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("main:create_academic_ajax")
        cls.regular = User.objects.create_user("regular", password="pw12345!")
        cls.editor = User.objects.create_user("editor", password="pw12345!")
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.owner = User.objects.create_superuser("owner", password="pw12345!")

    def test_owner_creates_academic_with_201(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, self.VALID)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Academic.objects.filter(pk=response.json()["pk"], institution="SMA Baru").exists())

    def test_invalid_input_returns_400_with_field_errors(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {**self.VALID, "institution": ""})

        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.json()["errors"])
        self.assertFalse(Academic.objects.exists())

    def test_visitor_regular_user_and_editor_get_403_json(self):
        # Visitor, user biasa, dan editor (editor tidak boleh membuat) ditolak dengan JSON, bukan redirect.
        for user in (None, self.regular, self.editor):
            if user:
                self.client.force_login(user)
            response = self.client.post(self.url, self.VALID)
            self.assertEqual(response.status_code, 403, user)
            self.assertIn("message", response.json())
        self.assertFalse(Academic.objects.exists())

    def test_get_is_not_allowed(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_csrf_token_is_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.url, self.VALID).status_code, 403)
        self.assertFalse(Academic.objects.exists())

        client.get(reverse("main:show_academic"))  # memasang cookie csrftoken
        token = client.cookies["csrftoken"].value
        response = client.post(self.url, self.VALID, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)


class AcademicXssProtectionTests(TestCase):
    PAYLOAD = "<img src=\"x\" onerror=\"alert('XSS!')\">"
    VALID = {"institution": "SMA Baru", "period": "2022 - 2025", "description": "Jurusan IPA", "order": 1}

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("main:create_academic_ajax")
        cls.owner = User.objects.create_superuser("owner", password="pw12345!")

    def setUp(self):
        self.client.force_login(self.owner)

    def test_payload_only_fields_are_rejected(self):
        for field in ("institution", "period", "description"):
            response = self.client.post(self.url, {**self.VALID, field: self.PAYLOAD})
            self.assertEqual(response.status_code, 400, field)
            self.assertIn(field, response.json()["errors"])
        self.assertFalse(Academic.objects.exists())

    def test_html_tags_are_stripped_from_mixed_input(self):
        response = self.client.post(
            self.url, {**self.VALID, "institution": "Halo <b>dunia</b><script>alert(1)</script>"}
        )

        self.assertEqual(response.status_code, 201)
        stored = Academic.objects.get(pk=response.json()["pk"])
        self.assertNotIn("<", stored.institution)
        self.assertTrue(stored.institution.startswith("Halo dunia"))

    def test_dangerous_image_urls_are_rejected(self):
        for image in ("javascript:alert(1)", "data:text/html,<script>alert(1)</script>", "//evil.example/x.png"):
            response = self.client.post(self.url, {**self.VALID, "image": image})
            self.assertEqual(response.status_code, 400, image)
            self.assertIn("image", response.json()["errors"])

    def test_valid_image_values_are_accepted(self):
        for image in ("", "/static/img/kuliah.jpeg", "https://example.com/logo.png"):
            response = self.client.post(self.url, {**self.VALID, "image": image})
            self.assertEqual(response.status_code, 201, image)
