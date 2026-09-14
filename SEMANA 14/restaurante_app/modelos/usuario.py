class Usuario:
    def __init__(self, nombre_usuario=None, contrasena="", rol="usuario", **kwargs):
        self.nombre_usuario = str(nombre_usuario or kwargs.get("usuario", kwargs.get("nombre", ""))).strip()
        self.contrasena = str(contrasena or kwargs.get("password", "")).strip()
        self.rol = str(rol or kwargs.get("rol", "usuario")).strip() or "usuario"
        self._validar()

    def _validar(self):
        if not self.nombre_usuario:
            raise ValueError("El nombre de usuario es obligatorio.")
        if not self.contrasena:
            raise ValueError("La contraseña es obligatoria.")

    def __str__(self):
        return f"{self.nombre_usuario} ({self.rol})"
