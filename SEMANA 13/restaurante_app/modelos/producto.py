class Producto:
	def __init__(self, nombre, precio, cantidad):
		self.nombre = nombre
		self.precio = float(precio)
		self.cantidad = int(cantidad)

	def __str__(self):
		return f"{self.nombre} - ${self.precio:.2f} - Stock: {self.cantidad}"
