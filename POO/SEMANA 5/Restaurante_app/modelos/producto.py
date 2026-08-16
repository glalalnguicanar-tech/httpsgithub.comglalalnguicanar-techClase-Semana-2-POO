"""Modelo Producto.

Implementa atributos con acceso controlado mediante @property y @setter,
con validaciones básicas solicitadas en la consigna.
"""

from typing import Any


class Producto:
    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True) -> None:
        # Usar los setters para aplicar validaciones desde la creación
        self._nombre: str = ""
        self._categoria: str = ""
        self._precio: float = 0.0
        self._disponible: bool = True

        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible

    # Nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # Categoria
    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # Precio
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: Any) -> None:
        try:
            precio_float = float(valor)
        except Exception:
            raise ValueError("El precio debe ser un número válido.")
        if precio_float <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = precio_float

    # Disponible
    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: Any) -> None:
        self._disponible = bool(valor)

    def mostrar_informacion(self) -> str:
        """Devuelve una cadena con la información del producto."""
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Nombre: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio:.2f} | {estado}"

    def __repr__(self) -> str:  # Representación útil para debugging
        return f"Producto(nombre={self.nombre!r}, categoria={self.categoria!r}, precio={self.precio!r}, disponible={self.disponible!r})"
