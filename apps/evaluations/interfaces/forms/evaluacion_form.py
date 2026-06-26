"""Formulario de alta/edición de evaluaciones."""

from django import forms

from apps.evaluations.models import Evaluacion


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ["titulo", "descripcion", "area_tema", "nivel_riesgo",
                  "umbral_aprobacion", "tiempo_limite_min"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "area_tema": forms.TextInput(attrs={"class": "form-control",
                                                "placeholder": "Ej. Uso de EPP, Trabajo en altura…"}),
            "nivel_riesgo": forms.Select(attrs={"class": "form-select"}),
            "umbral_aprobacion": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 100}),
            "tiempo_limite_min": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nivel_riesgo"].required = False
        self.fields["tiempo_limite_min"].required = False

    def clean_umbral_aprobacion(self):
        valor = self.cleaned_data["umbral_aprobacion"]
        if not (1 <= valor <= 100):
            raise forms.ValidationError("El umbral debe estar entre 1 y 100.")
        return valor
