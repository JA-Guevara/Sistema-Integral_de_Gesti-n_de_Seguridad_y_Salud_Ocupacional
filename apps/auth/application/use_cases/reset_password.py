"""CU-05 (solicitud): Caso de uso de recuperación de contraseña por email."""

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


class ResetPasswordUseCase:
    """Envía el correo con el enlace de recuperación de contraseña.

    Reutiliza `PasswordResetForm.save()`, que genera un token seguro por
    usuario y construye el enlace. La confirmación del token (paso final)
    se delega a la vista nativa `PasswordResetConfirmView` de Django, que
    ya valida el token de forma segura (no reinventamos esa lógica).
    """

    def send_reset_email(self, request, form):
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject_template_name='auth/password_reset_subject.txt',
            email_template_name='auth/password_reset_email.html',
            token_generator=default_token_generator,
        )
