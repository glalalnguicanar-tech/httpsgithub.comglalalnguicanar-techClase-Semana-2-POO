from datetime import datetime
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
	def __init__(self, archivo_servicio, ruta_productos, ruta_usuarios, ruta_ventas):
		self.archivo_servicio = archivo_servicio
		self.ruta_productos = Path(ruta_productos)
		self.ruta_usuarios = Path(ruta_usuarios)
		self.ruta_ventas = Path(ruta_ventas)
		self.productos = self._cargar_productos()
		self.usuarios = self._cargar_usuarios()
		self.ventas = self._cargar_ventas()

	def _cargar_productos(self):
		productos = []
		for datos in self.archivo_servicio.leer_json(self.ruta_productos):
			try:
				productos.append(Producto(**datos))
			except (TypeError, ValueError):
				continue
		return productos

	def _cargar_usuarios(self):
		usuarios = []
		for datos in self.archivo_servicio.leer_json(self.ruta_usuarios):
			try:
				usuarios.append(Usuario(**datos))
			except (TypeError, ValueError):
				continue
		return usuarios

	def _cargar_ventas(self):
		ventas = []
		for datos in self.archivo_servicio.leer_json(self.ruta_ventas):
			try:
				ventas.append(Venta(**datos))
			except (TypeError, ValueError):
				continue
		return ventas

	def _guardar_productos(self):
		self.archivo_servicio.guardar_json(self.ruta_productos, [p.to_dict() for p in self.productos])

	def _guardar_ventas(self):
		self.archivo_servicio.guardar_json(self.ruta_ventas, [v.to_dict() for v in self.ventas])

	def validar_acceso(self, nombre_usuario, contrasena):
		return any(u.nombre_usuario == nombre_usuario and u.contrasena == contrasena for u in self.usuarios)

	def listar_productos(self):
		return sorted(self.productos, key=lambda producto: producto.codigo.lower())

	def listar_usuarios(self):
		return list(self.usuarios)

	def listar_ventas(self):
		return list(self.ventas)

	def consultar_cantidad_productos(self):
		return sum(producto.cantidad for producto in self.productos)

	def registrar_producto(self, producto):
		if self.buscar_producto_por_codigo(producto.codigo):
			raise ValueError("Ya existe un producto con ese código.")
		self.productos.append(producto)
		self._guardar_productos()
		return producto

	def buscar_producto_por_codigo(self, codigo):
		codigo_buscar = str(codigo).strip().lower()
		return next((p for p in self.productos if p.codigo.lower() == codigo_buscar), None)

	def actualizar_producto(self, codigo, nombre=None, categoria=None, precio=None, cantidad=None):
		producto = self.buscar_producto_por_codigo(codigo)
		if producto is None:
			raise ValueError("No existe un producto con ese código.")
		if nombre is not None:
			producto.nombre = str(nombre).strip()
		if categoria is not None:
			producto.categoria = str(categoria).strip() or "general"
		if precio is not None:
			producto.precio = float(precio)
		if cantidad is not None:
			producto.cantidad = int(cantidad)
		producto._validar()
		self._guardar_productos()
		return producto

	def eliminar_producto(self, codigo):
		producto = self.buscar_producto_por_codigo(codigo)
		if producto is None:
			return False
		self.productos.remove(producto)
		self._guardar_productos()
		return True

	def registrar_venta(self, nombre_usuario, codigo_producto):
		usuario = next((u for u in self.usuarios if u.nombre_usuario == nombre_usuario), None)
		producto = self.buscar_producto_por_codigo(codigo_producto)
		if usuario is None:
			raise ValueError("Seleccione un usuario registrado.")
		if producto is None:
			raise ValueError("Seleccione un producto registrado.")
		if producto.cantidad <= 0:
			raise ValueError("El producto seleccionado no tiene existencias.")
		venta = Venta(usuario.nombre_usuario, producto.nombre, datetime.now().strftime("%Y-%m-%d %H:%M"))
		self.ventas.append(venta)
		self._guardar_ventas()
		return venta
