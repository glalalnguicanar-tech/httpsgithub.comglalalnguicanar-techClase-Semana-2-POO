from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
	def __init__(self, archivo_servicio, ruta_productos, ruta_usuarios):
		self.archivo_servicio = archivo_servicio
		self.productos = [
			Producto(**datos)
			for datos in archivo_servicio.leer_json(ruta_productos)
		]
		self.usuarios = [
			Usuario(**datos)
			for datos in archivo_servicio.leer_json(ruta_usuarios)
		]

	def validar_acceso(self, nombre_usuario, contrasena):
		return any(
			usuario.nombre_usuario == nombre_usuario
			and usuario.contrasena == contrasena
			for usuario in self.usuarios
		)

	def listar_productos(self):
		return list(self.productos)

	def listar_usuarios(self):
		return list(self.usuarios)

	def consultar_cantidad_productos(self):
		return sum(producto.cantidad for producto in self.productos)
