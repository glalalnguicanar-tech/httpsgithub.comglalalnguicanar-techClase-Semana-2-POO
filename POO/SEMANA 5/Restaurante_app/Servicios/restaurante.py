from typing import List

from ..modelos.cliente import Cliente
from ..modelos.producto import Producto


class Restaurante:
    def __init__(self) -> None:
        self.clientes: List[Cliente] = []
        self.productos: List[Producto] = []

    def agregar_cliente(self, cliente: Cliente) -> None:
        self.clientes.append(cliente)

    def eliminar_cliente(self, correo_electronico: str) -> bool:
        for cliente in self.clientes:
            if cliente.correo_electronico == correo_electronico:
                self.clientes.remove(cliente)
                return True
        return False

    def listar_clientes(self) -> List[Cliente]:
        return list(self.clientes)

    def agregar_producto(self, producto: Producto) -> None:
        self.productos.append(producto)

    def eliminar_producto(self, nombre_producto: str) -> bool:
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                self.productos.remove(producto)
                return True
        return False

    def listar_productos(self) -> List[Producto]:
        return list(self.productos)

    def buscar_producto_por_categoria(self, categoria: str) -> List[Producto]:
        return [producto for producto in self.productos if producto.categoria == categoria]

    def buscar_cliente_por_nombre(self, nombre: str) -> List[Cliente]:
        return [cliente for cliente in self.clientes if cliente.nombre == nombre]

    def __repr__(self) -> str:
        return (
            f"Restaurante(clientes={len(self.clientes)}, productos={len(self.productos)})"
        )
 