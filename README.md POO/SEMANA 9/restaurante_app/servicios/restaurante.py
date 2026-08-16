from __future__ import annotations

from modelos.producto import Producto
from modelos.usuario import Usuario


class Restaurante:
    """Administra los productos, usuarios y operaciones del sistema."""

    def __init__(self) -> None:
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.opciones_menu: tuple[str, ...] = (
            "1. Registrar producto",
            "2. Buscar producto",
            "3. Actualizar producto",
            "4. Eliminar producto",
            "5. Listar productos",
            "6. Registrar usuario",
            "7. Listar usuarios",
            "8. Mostrar categorías",
            "9. Salir",
        )
        self.acciones_menu: dict[str, str] = {
            "1": "Registrar producto",
            "2": "Buscar producto",
            "3": "Actualizar producto",
            "4": "Eliminar producto",
            "5": "Listar productos",
            "6": "Registrar usuario",
            "7": "Listar usuarios",
            "8": "Mostrar categorías",
            "9": "Salir",
        }

    def registrar_producto(self, producto: Producto) -> bool:
        for producto_registrado in self.productos:
            if producto_registrado.codigo.lower() == producto.codigo.lower():
                raise ValueError("El código del producto ya existe.")

        self.productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo_buscar = codigo.strip().lower()
        for producto in self.productos:
            if producto.codigo.lower() == codigo_buscar:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str | None = None,
        categoria: str | None = None,
        precio: float | None = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        if nombre is not None and nombre.strip():
            producto.nombre = nombre.strip()
        if categoria is not None and categoria.strip():
            producto.categoria = categoria.strip()
        if precio is not None:
            producto.precio = precio

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        codigo_buscar = codigo.strip().lower()
        for indice, producto in enumerate(self.productos):
            if producto.codigo.lower() == codigo_buscar:
                del self.productos[indice]
                return True
        return False

    def listar_productos(self) -> list[Producto]:
        return self.productos

    def registrar_usuario(self, usuario: Usuario) -> bool:
        for usuario_registrado in self.usuarios:
            if usuario_registrado.identificacion.lower() == usuario.identificacion.lower():
                raise ValueError("La identificación del usuario ya existe.")

        self.usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def mostrar_categorias(self) -> set[str]:
        categorias: set[str] = set()
        for producto in self.productos:
            categorias.add(producto.categoria.lower())
        return categorias
