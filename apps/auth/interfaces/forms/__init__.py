"""Shared form helpers for the authentication app."""

from django import forms


class BootstrapFormMixin:
    """Apply Bootstrap 5 classes to Django form widgets."""

    default_class = "form-control"
    checkbox_class = "form-check-input"
    select_class = "form-select"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()

    def _apply_bootstrap_classes(self):
        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.HiddenInput):
                continue

            if isinstance(widget, forms.CheckboxInput):
                css_class = self.checkbox_class
            elif isinstance(widget, forms.Select):
                css_class = self.select_class
            else:
                css_class = self.default_class

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()


__all__ = ["BootstrapFormMixin"]
