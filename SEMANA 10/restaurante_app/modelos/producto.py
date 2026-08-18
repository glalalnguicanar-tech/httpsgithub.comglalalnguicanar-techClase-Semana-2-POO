from __future__ import annotations


class Producto:
    """Representa un producto del restaurante."""

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = precio
        self._validar()

    def _validar(self) -> None:
        """Valida los atributos del producto."""
        if not self.codigo:
            raise ValueError("El código del producto no puede estar vacío.")
        if not self.nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not self.categoria:
            raise ValueError("La categoría del producto no puede estar vacía.")
        if self.precio < 0:
            raise ValueError("El precio del producto no puede ser negativo.")

    def to_dict(self) -> dict[str, str | float]:
        """Convierte el producto a un diccionario para almacenamiento JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
        }

    @staticmethod
    def from_dict(datos: dict[str, str | float]) -> Producto:
        """Crea un producto a partir de un diccionario."""
        try:
            return Producto(
                codigo=str(datos["codigo"]),
                nombre=str(datos["nombre"]),
                categoria=str(datos["categoria"]),
                precio=float(datos["precio"]),
            )
        except KeyError as e:
            raise ValueError(f"Registro incompleto: falta la clave {e}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Error al reconstruir producto: {e}")

    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: ${self.precio:.2f}"
        )
