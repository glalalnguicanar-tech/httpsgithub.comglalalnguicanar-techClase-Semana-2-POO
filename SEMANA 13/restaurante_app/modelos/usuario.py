class Usuario:
	def __init__(self, nombre_usuario, contrasena, rol="usuario"):
		self.nombre_usuario = nombre_usuario
		self.contrasena = contrasena
		self.rol = rol

	def __str__(self):
		return f"{self.nombre_usuario} ({self.rol})"
