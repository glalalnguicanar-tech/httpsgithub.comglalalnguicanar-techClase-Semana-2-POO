"""Servicio Restaurante: administra productos y clientes (SEMANA 7)."""

from typing import List, Optional
from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    def registrar_producto(self, producto: Producto) -> None:
        if any(p.nombre.lower() == producto.nombre.lower() for p in self._productos):
            raise ValueError("Ya existe un producto con ese nombre.")
        self._productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        return list(self._productos)

    def buscar_producto(self, nombre: str) -> Optional[Producto]:
        nombre = nombre.strip().lower()
        for p in self._productos:
            if p.nombre.lower() == nombre:
                return p
        return None

    def registrar_cliente(self, cliente: Cliente) -> None:
        if any(c.id_cliente == cliente.id_cliente for c in self._clientes):
            raise ValueError("Ya existe un cliente con ese ID.")
        self._clientes.append(cliente)

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes)

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        id_cliente = id_cliente.strip()
        for c in self._clientes:
            if c.id_cliente == id_cliente:
                return c
        return None
"""Servicio Restaurante (archivo heredado en carpeta `Servicios`).

Este archivo está en la carpeta `Servicios` con S mayúscula; la versión
canónica se encuentra en `servicios/restaurante.py`. No modificaré
esta copia vacía para no romper imports existentes.
"""
