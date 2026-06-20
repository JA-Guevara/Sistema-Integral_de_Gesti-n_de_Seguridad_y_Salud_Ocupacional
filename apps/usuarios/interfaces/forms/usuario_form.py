"""Formulario de alta/edición de usuarios."""

from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password


class UsuarioForm(forms.ModelForm):
    """ModelForm sobre `auth.User` con campos de contraseña y roles (groups).

    - Al CREAR (`require_password=True`) la contraseña es obligatoria.
    - Al EDITAR, dejarla en blanco mantiene la contraseña actual.
    - `groups` es el campo nativo de roles; se muestra como checkboxes.
    """

    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'groups']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'groups': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'is_active': 'Activo',
            'groups': 'Roles',
        }

    def __init__(self, *args, require_password=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.order_by('name')
        self.fields['groups'].required = False
        if require_password:
            self.fields['password'].required = True
        else:
            self.fields['password'].help_text = 'Déjalo en blanco para no cambiar la contraseña.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if email and qs.exists():
            raise forms.ValidationError('Ya existe otro usuario con ese correo electrónico.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password, self.instance)  # política de contraseñas de Django
        return password
