from __future__ import annotations
from typing import List, Optional

from modelos.cliente import Cliente
from modelos.producto import Producto

class Restaurante:
    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    def registrar_producto(self, producto: Producto) -> bool:
        if self._buscar_producto_por_codigo(producto.codigo) is not None:
            return False
        self._productos.append(producto)
        return True

    def registrar_cliente(self, cliente: Cliente) -> bool:
        if self._buscar_cliente_por_identificacion(cliente.identificacion) is not None:
            return False
        self._clientes.append(cliente)
        return True

    def listar_productos(self) -> List[str]:
        return [producto.mostrar_informacion() for producto in self._productos]

    def listar_clientes(self) -> List[str]:
        return [cliente.mostrar_informacion() for cliente in self._clientes]

    def _buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def _buscar_cliente_por_identificacion(self, identificacion: str) -> Optional[Cliente]:
        for cliente in self._clientes:
            if cliente.identificacion == identificacion:
                return cliente
        return None
