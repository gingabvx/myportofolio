from django.forms import ModelForm, TextInput, Textarea, Select

from main.models import Projects

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