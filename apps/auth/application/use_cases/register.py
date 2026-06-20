"""CU-03: Caso de uso de registro de usuarios."""


class RegisterUseCase:
    """Crea un nuevo usuario a partir de un formulario ya validado.

    Es el punto donde, a futuro, se podrían añadir efectos secundarios
    (enviar correo de bienvenida, crear un perfil asociado, etc.) sin
    tocar la vista. Hoy se mantiene simple para evitar sobreingeniería.
    """

    def execute(self, form):
        # El formulario (basado en UserCreationForm) cifra la contraseña
        # y persiste el usuario con todos sus datos.
        user = form.save()
        return user
