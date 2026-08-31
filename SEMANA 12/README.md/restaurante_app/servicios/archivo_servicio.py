from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
	"""Centraliza la persistencia JSON de las tres colecciones."""

	def __init__(self, directorio: str | Path) -> None:
		self.directorio = Path(directorio)
		self.directorio.mkdir(parents=True, exist_ok=True)
		self.rutas = {
			"productos": self.directorio / "productos.json",
			"usuarios": self.directorio / "usuarios.json",
			"ventas": self.directorio / "ventas.json",
		}

	def _cargar(
		self, nombre: str, reconstruir: Callable[[dict[str, object]], Any]
	) -> list[Any]:
		ruta = self.rutas[nombre]
		if not ruta.exists():
			return []
		try:
			with open(ruta, "r", encoding="utf-8") as archivo:
				datos = json.load(archivo)
		except PermissionError as error:
			raise PermissionError(f"No hay permisos para leer {ruta}.") from error
		if not isinstance(datos, list):
			raise ValueError(f"{ruta.name} debe contener una lista JSON.")

		registros: list[Any] = []
		for indice, registro in enumerate(datos):
			if not isinstance(registro, dict):
				raise ValueError(f"Registro inválido en {ruta.name}, posición {indice}.")
			try:
				registros.append(reconstruir(registro))
			except ValueError as error:
				raise ValueError(
					f"Registro inválido en {ruta.name}, posición {indice}: {error}"
				) from error
		return registros

	def _guardar(self, nombre: str, objetos: list[Any]) -> None:
		ruta = self.rutas[nombre]
		datos = [objeto.to_dict() for objeto in objetos]
		try:
			with open(ruta, "w", encoding="utf-8") as archivo:
				json.dump(datos, archivo, indent=4, ensure_ascii=False)
		except PermissionError as error:
			raise PermissionError(f"No hay permisos para escribir {ruta}.") from error

	def cargar_productos(self) -> list[Producto]:
		return self._cargar("productos", Producto.from_dict)

	def cargar_usuarios(self) -> list[Usuario]:
		return self._cargar("usuarios", Usuario.from_dict)

	def cargar_ventas(self) -> list[Venta]:
		return self._cargar("ventas", Venta.from_dict)

	def guardar_productos(self, productos: list[Producto]) -> None:
		self._guardar("productos", productos)

	def guardar_usuarios(self, usuarios: list[Usuario]) -> None:
		self._guardar("usuarios", usuarios)

	def guardar_ventas(self, ventas: list[Venta]) -> None:
		self._guardar("ventas", ventas)

	def guardar_todo(
		self,
		productos: list[Producto],
		usuarios: list[Usuario],
		ventas: list[Venta],
	) -> None:
		self.guardar_productos(productos)
		self.guardar_usuarios(usuarios)
		self.guardar_ventas(ventas)
