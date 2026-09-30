from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput
from django.utils.html import strip_tags

from main.models import Projects, Academic

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = [
            "title",
            "description",
            "category",
            "status",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "category": "Project Category",
            "status": "Project Status",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Website Portofolio",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your project",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi proyek tidak boleh hanya berisi tag HTML.")
        return description


class AcademicForm(ModelForm):
    class Meta:
        model = Academic
        fields = [
            "institution",
            "period",
            "description",
            "image",
            "order",
        ]

        labels = {
            "institution": "Institution / School Name",
            "period": "Years / Period",
            "description": "Description",
            "image": "Logo / Image URL (Optional)",
            "order": "Order",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "ex: Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "period": TextInput(
                attrs={
                    "placeholder": "ex: 2025 - Present",
                    "maxlength": 100,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your academic background.",
                    "rows": 3,
                }
            ),
            "image": TextInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                    "maxlength": 255,
                }
            ),
            "order": NumberInput(
                attrs={
                    "placeholder": "0",
                    "min": 0,
                }
            ),
        }