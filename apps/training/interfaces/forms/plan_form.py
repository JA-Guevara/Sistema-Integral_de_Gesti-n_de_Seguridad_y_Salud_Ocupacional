"""Formulario de alta/edición de planes de capacitación."""

from django import forms

from apps.training.models import PlanCapacitacion


class PlanForm(forms.ModelForm):
    class Meta:
        model = PlanCapacitacion
        fields = ["titulo", "descripcion", "area_tema", "material_url"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "area_tema": forms.TextInput(attrs={"class": "form-control"}),
            "material_url": forms.URLInput(attrs={"class": "form-control",
                                                  "placeholder": "https://… (video, PDF, curso)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["material_url"].required = False
