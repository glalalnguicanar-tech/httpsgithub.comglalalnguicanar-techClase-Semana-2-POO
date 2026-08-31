from __future__ import annotations

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
	"""Administra las colecciones con índices para optimizar búsquedas frecuentes."""

	def __init__(self) -> None:
		# Colecciones principales para persistencia y recorrido
		self._productos: list[Producto] = []
		self._usuarios: list[Usuario] = []
		self._ventas: list[Venta] = []

		# Índices auxiliares para búsquedas rápidas por clave
		self._productos_por_codigo: dict[str, Producto] = {}
		self._usuarios_por_id: dict[str, Usuario] = {}
		self._ventas_por_usuario: dict[str, list[Venta]] = {}

	def cargar_datos(
		self,
		productos: list[Producto],
		usuarios: list[Usuario],
		ventas: list[Venta],
	) -> None:
		"""Carga los datos y reconstruye los índices desde las colecciones principales."""
		self._productos = productos
		self._usuarios = usuarios
		self._ventas = ventas
		self._reconstruir_indices()

	def _reconstruir_indices(self) -> None:
		"""Reconstruye todos los índices desde las colecciones principales."""
		# Reconstruir índice de productos
		self._productos_por_codigo.clear()
		for producto in self._productos:
			codigo_lower = producto.codigo.lower()
			self._productos_por_codigo[codigo_lower] = producto

		# Reconstruir índice de usuarios
		self._usuarios_por_id.clear()
		for usuario in self._usuarios:
			id_lower = usuario.identificacion.lower()
			self._usuarios_por_id[id_lower] = usuario

		# Reconstruir índice de ventas por usuario
		self._ventas_por_usuario.clear()
		for venta in self._ventas:
			usuario_lower = venta.usuario_id.lower()
			if usuario_lower not in self._ventas_por_usuario:
				self._ventas_por_usuario[usuario_lower] = []
			self._ventas_por_usuario[usuario_lower].append(venta)

	def registrar_producto(self, producto: Producto) -> bool:
		"""Registra un producto y actualiza el índice."""
		if self.buscar_producto(producto.codigo) is not None:
			raise ValueError("El código del producto ya existe.")
		self._productos.append(producto)
		codigo_lower = producto.codigo.lower()
		self._productos_por_codigo[codigo_lower] = producto
		return True

	def buscar_producto(self, codigo: str) -> Producto | None:
		"""Busca un producto por código usando el índice (O(1) en lugar de O(n))."""
		codigo_lower = codigo.strip().lower()
		return self._productos_por_codigo.get(codigo_lower)

	def actualizar_producto(
		self,
		codigo: str,
		nombre: str | None = None,
		categoria: str | None = None,
		precio: float | None = None,
		stock: int | None = None,
	) -> bool:
		"""Actualiza un producto encontrado por el índice."""
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
		"""Elimina un producto y actualiza el índice."""
		producto = self.buscar_producto(codigo)
		if producto is None:
			return False
		self._productos.remove(producto)
		codigo_lower = codigo.strip().lower()
		del self._productos_por_codigo[codigo_lower]
		return True

	def listar_productos(self) -> list[Producto]:
		"""Retorna la lista principal de productos."""
		return self._productos

	def registrar_usuario(self, usuario: Usuario) -> bool:
		"""Registra un usuario y actualiza el índice."""
		if self.buscar_usuario(usuario.identificacion) is not None:
			raise ValueError("La identificación del usuario ya existe.")
		self._usuarios.append(usuario)
		id_lower = usuario.identificacion.lower()
		self._usuarios_por_id[id_lower] = usuario
		return True

	def buscar_usuario(self, identificacion: str) -> Usuario | None:
		"""Busca un usuario por identificación usando el índice (O(1) en lugar de O(n))."""
		id_lower = identificacion.strip().lower()
		return self._usuarios_por_id.get(id_lower)

	def listar_usuarios(self) -> list[Usuario]:
		"""Retorna la lista principal de usuarios."""
		return self._usuarios

	def vender_producto(
		self, codigo_producto: str, identificacion_usuario: str, cantidad: int
	) -> bool:
		"""Realiza una venta y actualiza índices."""
		usuario = self.buscar_usuario(identificacion_usuario)
		producto = self.buscar_producto(codigo_producto)
		if usuario is None or producto is None:
			return False
		if cantidad <= 0 or producto.stock < cantidad:
			return False

		venta = Venta(usuario.identificacion, producto.codigo, cantidad)
		self._ventas.append(venta)
		
		# Actualizar índice de ventas por usuario
		usuario_lower = usuario.identificacion.lower()
		if usuario_lower not in self._ventas_por_usuario:
			self._ventas_por_usuario[usuario_lower] = []
		self._ventas_por_usuario[usuario_lower].append(venta)
		
		producto.vender(cantidad)
		return True

	def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
		"""Consulta ventas de un usuario usando el índice (O(1) en lugar de O(n))."""
		id_lower = identificacion_usuario.strip().lower()
		return self._ventas_por_usuario.get(id_lower, [])

	def listar_ventas(self) -> list[Venta]:
		"""Retorna la lista principal de ventas."""
		return self._ventas

	def mostrar_categorias(self) -> set[str]:
		"""Retorna el conjunto de categorías disponibles."""
		return {producto.categoria.lower() for producto in self._productos}
