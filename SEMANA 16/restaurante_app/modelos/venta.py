class Venta:
	def __init__(self, usuario, producto, fecha):
		self.usuario = str(usuario).strip()
		self.producto = str(producto).strip()
		self.fecha = str(fecha).strip()
		if not self.usuario or not self.producto or not self.fecha:
			raise ValueError("La venta requiere usuario, producto y fecha.")

	def to_dict(self):
		return {"usuario": self.usuario, "producto": self.producto, "fecha": self.fecha}
