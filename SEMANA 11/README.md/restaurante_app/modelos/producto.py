from __future__ import annotations


class Producto:
	"""Representa un producto disponible en el restaurante."""

	def __init__(
		self,
		codigo: str,
		nombre: str,
		categoria: str,
		precio: float,
		stock: int = 0,
	) -> None:
		self.codigo = codigo.strip()
		self.nombre = nombre.strip()
		self.categoria = categoria.strip()
		self.precio = float(precio)
		self.stock = int(stock)
		self._validar()

	def _validar(self) -> None:
		if not self.codigo or not self.nombre or not self.categoria:
			raise ValueError("Código, nombre y categoría son obligatorios.")
		if self.precio < 0:
			raise ValueError("El precio no puede ser negativo.")
		if self.stock < 0:
			raise ValueError("El stock no puede ser negativo.")

	def vender(self, cantidad: int) -> None:
		"""Descuenta una cantidad validada del stock disponible."""
		if cantidad <= 0:
			raise ValueError("La cantidad debe ser mayor que cero.")
		if cantidad > self.stock:
			raise ValueError("No hay stock suficiente.")
		self.stock -= cantidad

	def to_dict(self) -> dict[str, str | float | int]:
		return {
			"codigo": self.codigo,
			"nombre": self.nombre,
			"categoria": self.categoria,
			"precio": self.precio,
			"stock": self.stock,
		}

	@staticmethod
	def from_dict(datos: dict[str, object]) -> Producto:
		try:
			return Producto(
				codigo=str(datos["codigo"]),
				nombre=str(datos["nombre"]),
				categoria=str(datos["categoria"]),
				precio=float(datos["precio"]),
				stock=int(datos.get("stock", 0)),
			)
		except KeyError as error:
			raise ValueError(f"Registro incompleto: falta la clave {error}") from error
		except (TypeError, ValueError) as error:
			raise ValueError(f"Error al reconstruir producto: {error}") from error

	def __str__(self) -> str:
		return (
			f"Código: {self.codigo} | Nombre: {self.nombre} | "
			f"Categoría: {self.categoria} | Precio: ${self.precio:.2f} | "
			f"Stock: {self.stock}"
		)
