from __future__ import annotations

from modelos.producto import Producto
from modelos.usuario import Usuario


class Restaurante:
    """Administra los productos, usuarios y operaciones del sistema."""

    def __init__(self) -> None:
        """Inicializa el restaurante con colecciones vacías y opciones de menú."""
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

    def cargar_productos_iniciales(self, productos: list[Producto]) -> None:
        """
        Carga una lista inicial de productos (típicamente desde archivo JSON).

        Args:
            productos: Lista de objetos Producto a cargar.
        """
        self.productos = productos

    def registrar_producto(self, producto: Producto) -> bool:
        """
        Registra un nuevo producto en la colección.

        Args:
            producto: Objeto Producto a registrar.

        Retorna:
            True si el registro fue exitoso.

        Excepciones:
            ValueError: Si el código del producto ya existe.
        """
        for producto_registrado in self.productos:
            if producto_registrado.codigo.lower() == producto.codigo.lower():
                raise ValueError("El código del producto ya existe.")

        self.productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        """
        Busca un producto por su código.

        Args:
            codigo: Código del producto a buscar.

        Retorna:
            El objeto Producto si lo encuentra, None en caso contrario.
        """
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
        """
        Actualiza los atributos de un producto existente.

        Args:
            codigo: Código del producto a actualizar.
            nombre: Nuevo nombre (opcional).
            categoria: Nueva categoría (opcional).
            precio: Nuevo precio (opcional).

        Retorna:
            True si la actualización fue exitosa, False si no encontró el producto.
        """
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

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto de la colección.

        Args:
            codigo: Código del producto a eliminar.

        Retorna:
            True si la eliminación fue exitosa, False si no encontró el producto.
        """
        codigo_buscar = codigo.strip().lower()
        for indice, producto in enumerate(self.productos):
            if producto.codigo.lower() == codigo_buscar:
                del self.productos[indice]
                return True
        return False

    def listar_productos(self) -> list[Producto]:
        """
        Retorna la lista completa de productos.

        Retorna:
            Lista de objetos Producto.
        """
        return self.productos

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en la colección.

        Args:
            usuario: Objeto Usuario a registrar.

        Retorna:
            True si el registro fue exitoso.

        Excepciones:
            ValueError: Si la identificación del usuario ya existe.
        """
        for usuario_registrado in self.usuarios:
            if usuario_registrado.identificacion.lower() == usuario.identificacion.lower():
                raise ValueError("La identificación del usuario ya existe.")

        self.usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        """
        Retorna la lista completa de usuarios.

        Retorna:
            Lista de objetos Usuario.
        """
        return self.usuarios

    def mostrar_categorias(self) -> set[str]:
        """
        Retorna el conjunto de categorías únicas de los productos.

        Retorna:
            Conjunto con las categorías en minúscula.
        """
        categorias: set[str] = set()
        for producto in self.productos:
            categorias.add(producto.categoria.lower())
        return categorias
