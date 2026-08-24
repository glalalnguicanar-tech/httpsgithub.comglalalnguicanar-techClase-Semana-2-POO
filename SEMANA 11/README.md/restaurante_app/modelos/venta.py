from __future__ import annotations


class Venta:
	"""Representa la relación entre un usuario y un producto vendido."""

	def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
		self.usuario_id = usuario_id.strip()
		self.producto_codigo = producto_codigo.strip()
		self.cantidad = int(cantidad)
		self._validar()

	def _validar(self) -> None:
		if not self.usuario_id or not self.producto_codigo:
			raise ValueError("El usuario y el producto son obligatorios.")
		if self.cantidad <= 0:
			raise ValueError("La cantidad vendida debe ser mayor que cero.")

	def to_dict(self) -> dict[str, str | int]:
		return {
			"usuario_id": self.usuario_id,
			"producto_codigo": self.producto_codigo,
			"cantidad": self.cantidad,
		}

	@staticmethod
	def from_dict(datos: dict[str, object]) -> Venta:
		try:
			return Venta(
				usuario_id=str(datos["usuario_id"]),
				producto_codigo=str(datos["producto_codigo"]),
				cantidad=int(datos["cantidad"]),
			)
		except KeyError as error:
			raise ValueError(f"Registro incompleto: falta la clave {error}") from error

	def __str__(self) -> str:
		return (
			f"Usuario: {self.usuario_id} | Producto: {self.producto_codigo} | "
			f"Cantidad: {self.cantidad}"
		)
