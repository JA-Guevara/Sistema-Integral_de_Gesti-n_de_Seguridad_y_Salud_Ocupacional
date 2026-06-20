"""Formularios del módulo de autenticación.

Define un mixin reutilizable para aplicar las clases de Bootstrap 5 a
cualquier formulario, evitando repetir estilos campo por campo (DRY).
"""


class BootstrapFormMixin:
    """Aplica clases de Bootstrap 5 a todos los campos del formulario.

    Debe declararse ANTES que la clase de formulario en la herencia, p. ej.:
        class LoginForm(BootstrapFormMixin, forms.Form): ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            # Usa la etiqueta del campo como placeholder si no hay uno definido.
            field.widget.attrs.setdefault('placeholder', field.label)
