class Usuario:
	ROLES = ("Administrador", "Empleado", "Cliente")

	def __init__(self, nombre_usuario=None, contrasena="", rol="Empleado", id=None, nombre=None, **kwargs):
		self.id = int(id) if id not in (None, "") else None
		self.nombre_usuario = str(nombre_usuario or kwargs.get("usuario", "")).strip()
		self.nombre = str(nombre or kwargs.get("nombre", self.nombre_usuario)).strip()
		self.contrasena = str(contrasena or kwargs.get("password", "")).strip()
		rol_normalizado = str(rol or "Empleado").strip().casefold()
		self.rol = {"administrador": "Administrador", "admin": "Administrador", "empleado": "Empleado", "usuario": "Empleado", "cliente": "Cliente"}.get(rol_normalizado, "Empleado")
		if not self.nombre_usuario or not self.nombre or not self.contrasena:
			raise ValueError("El nombre, usuario y contraseña son obligatorios.")
		if self.id is not None and self.id < 1:
			raise ValueError("El identificador del usuario debe ser positivo.")

	def to_dict(self):
		return {"id": self.id, "nombre": self.nombre, "nombre_usuario": self.nombre_usuario,
				"contrasena": self.contrasena, "rol": self.rol}

	def __str__(self):
		return f"{self.nombre} ({self.rol})"
