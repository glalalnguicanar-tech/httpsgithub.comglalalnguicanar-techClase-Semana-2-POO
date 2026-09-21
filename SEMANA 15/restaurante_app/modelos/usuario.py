class Usuario:
	def __init__(self, nombre_usuario=None, contrasena="", rol="usuario", **kwargs):
		self.nombre_usuario = str(nombre_usuario or kwargs.get("usuario", kwargs.get("nombre", ""))).strip()
		self.contrasena = str(contrasena or kwargs.get("password", "")).strip()
		self.rol = str(rol or kwargs.get("rol", "usuario")).strip() or "usuario"
		if not self.nombre_usuario or not self.contrasena:
			raise ValueError("El usuario y la contraseña son obligatorios.")

	def __str__(self):
		return f"{self.nombre_usuario} ({self.rol})"
