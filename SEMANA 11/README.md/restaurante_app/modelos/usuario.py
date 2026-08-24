from __future__ import annotations


class Usuario:
	"""Representa a una persona que puede realizar compras."""

	def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
		self.identificacion = identificacion.strip()
		self.nombre = nombre.strip()
		self.correo = correo.strip()
		self._validar()

	def _validar(self) -> None:
		if not self.identificacion or not self.nombre or not self.correo:
			raise ValueError("Identificación, nombre y correo son obligatorios.")

	def to_dict(self) -> dict[str, str]:
		return {
			"identificacion": self.identificacion,
			"nombre": self.nombre,
			"correo": self.correo,
		}

	@staticmethod
	def from_dict(datos: dict[str, object]) -> Usuario:
		try:
			return Usuario(
				identificacion=str(datos["identificacion"]),
				nombre=str(datos["nombre"]),
				correo=str(datos["correo"]),
			)
		except KeyError as error:
			raise ValueError(f"Registro incompleto: falta la clave {error}") from error

	def __str__(self) -> str:
		return (
			f"Identificación: {self.identificacion} | "
			f"Nombre: {self.nombre} | Correo: {self.correo}"
		)
