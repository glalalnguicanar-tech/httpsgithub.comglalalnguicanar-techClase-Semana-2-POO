from __future__ import annotations

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
	"""Administra las colecciones y las reglas de negocio."""

	def __init__(self) -> None:
		self._productos: list[Producto] = []
		self._usuarios: list[Usuario] = []
		self._ventas: list[Venta] = []

	def cargar_datos(
		self,
		productos: list[Producto],
		usuarios: list[Usuario],
		ventas: list[Venta],
	) -> None:
		self._productos = productos
		self._usuarios = usuarios
		self._ventas = ventas

	def registrar_producto(self, producto: Producto) -> bool:
		if self.buscar_producto(producto.codigo) is not None:
			raise ValueError("El código del producto ya existe.")
		self._productos.append(producto)
		return True

	def buscar_producto(self, codigo: str) -> Producto | None:
		codigo_buscado = codigo.strip().lower()
		for producto in self._productos:
			if producto.codigo.lower() == codigo_buscado:
				return producto
		return None

	def actualizar_producto(
		self,
		codigo: str,
		nombre: str | None = None,
		categoria: str | None = None,
		precio: float | None = None,
		stock: int | None = None,
	) -> bool:
		producto = self.buscar_producto(codigo)
		if producto is None:
			return False
		if nombre is not None and nombre.strip():
			producto.nombre = nombre.strip()
		if categoria is not None and categoria.strip():
			producto.categoria = categoria.strip()
		if precio is not None:
			if precio < 0:
				raise ValueError("El precio no puede ser negativo.")
			producto.precio = precio
		if stock is not None:
			if stock < 0:
				raise ValueError("El stock no puede ser negativo.")
			producto.stock = stock
		return True

	def eliminar_producto(self, codigo: str) -> bool:
		producto = self.buscar_producto(codigo)
		if producto is None:
			return False
		self._productos.remove(producto)
		return True

	def listar_productos(self) -> list[Producto]:
		return self._productos

	def registrar_usuario(self, usuario: Usuario) -> bool:
		if self.buscar_usuario(usuario.identificacion) is not None:
			raise ValueError("La identificación del usuario ya existe.")
		self._usuarios.append(usuario)
		return True

	def buscar_usuario(self, identificacion: str) -> Usuario | None:
		identificacion_buscada = identificacion.strip().lower()
		for usuario in self._usuarios:
			if usuario.identificacion.lower() == identificacion_buscada:
				return usuario
		return None

	def listar_usuarios(self) -> list[Usuario]:
		return self._usuarios

	def vender_producto(
		self, codigo_producto: str, identificacion_usuario: str, cantidad: int
	) -> bool:
		usuario = self.buscar_usuario(identificacion_usuario)
		producto = self.buscar_producto(codigo_producto)
		if usuario is None or producto is None:
			return False
		if cantidad <= 0 or producto.stock < cantidad:
			return False

		venta = Venta(usuario.identificacion, producto.codigo, cantidad)
		self._ventas.append(venta)
		producto.vender(cantidad)
		return True

	def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
		ventas_usuario: list[Venta] = []
		identificacion_buscada = identificacion_usuario.strip().lower()
		for venta in self._ventas:
			if venta.usuario_id.lower() == identificacion_buscada:
				ventas_usuario.append(venta)
		return ventas_usuario

	def listar_ventas(self) -> list[Venta]:
		return self._ventas

	def mostrar_categorias(self) -> set[str]:
		return {producto.categoria.lower() for producto in self._productos}
