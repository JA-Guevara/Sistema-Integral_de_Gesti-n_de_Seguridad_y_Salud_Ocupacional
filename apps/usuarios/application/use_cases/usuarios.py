"""Casos de uso de USUARIOS (sobre `auth.User`, roles vía `user.groups`)."""

from django.contrib.auth.models import Group, User

from apps.usuarios.application.use_cases.exceptions import UsuarioError


class ListarUsuarios:
    """Lista los usuarios con sus roles (grupos) precargados."""

    def execute(self):
        return User.objects.prefetch_related('groups').order_by(
            'first_name', 'last_name', 'username'
        )


class ObtenerUsuario:
    """Recupera un usuario por id o lanza error de negocio."""

    def execute(self, user_id):
        try:
            return User.objects.prefetch_related('groups').get(pk=user_id)
        except User.DoesNotExist:
            raise UsuarioError('El usuario solicitado no existe.')


class CrearUsuario:
    """Crea un usuario a partir de un UsuarioForm ya validado."""

    def execute(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # contraseña obligatoria al crear
        user.save()
        form.save_m2m()  # guarda los roles (groups) seleccionados
        return user


class ActualizarUsuario:
    """Actualiza un usuario; la contraseña solo cambia si se ingresó una nueva."""

    def execute(self, form):
        user = form.save(commit=False)
        nueva_password = form.cleaned_data.get('password')
        if nueva_password:
            user.set_password(nueva_password)
        user.save()
        form.save_m2m()
        return user


class CambiarEstadoUsuario:
    """Activa/desactiva un usuario. No permite que alguien se desactive a sí mismo."""

    def execute(self, user_id, actor_id=None):
        user = ObtenerUsuario().execute(user_id)
        if user.is_active and actor_id is not None and user.pk == actor_id:
            raise UsuarioError('No puedes desactivar tu propio usuario.')
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return user


class ResetearPasswordUsuario:
    """Envía al usuario un enlace de recuperación, reutilizando el flujo de `auth`."""

    def execute(self, request, user_id):
        user = ObtenerUsuario().execute(user_id)
        if not user.is_active:
            raise UsuarioError('No se puede enviar el enlace a un usuario inactivo.')
        if not user.email:
            raise UsuarioError('El usuario no tiene un correo registrado.')

        # Reutilizamos el formulario y caso de uso del módulo de autenticación.
        from apps.auth.application.use_cases.reset_password import ResetPasswordUseCase
        from apps.auth.interfaces.forms.password_form import StyledPasswordResetForm

        form = StyledPasswordResetForm({'email': user.email})
        if not form.is_valid():
            raise UsuarioError('El correo del usuario no es válido.')
        ResetPasswordUseCase().send_reset_email(request, form)
        return user


class AsignarRolMasivo:
    """Asigna un rol activo a varios usuarios activos a la vez."""

    def execute(self, *, rol_id, user_ids):
        try:
            grupo = Group.objects.select_related('perfil').get(pk=rol_id)
        except Group.DoesNotExist:
            raise UsuarioError('El rol seleccionado no existe.')

        perfil = getattr(grupo, 'perfil', None)
        if perfil is not None and not perfil.activo:
            raise UsuarioError('No puedes asignar un rol inactivo.')

        usuarios = list(User.objects.filter(pk__in=user_ids, is_active=True))
        if not usuarios:
            raise UsuarioError('Selecciona al menos un usuario activo.')

        for user in usuarios:
            user.groups.add(grupo)
        return len(usuarios)
