"""Modelo Cliente usando @dataclass."""

from dataclasses import dataclass


@dataclass
class Cliente:
    nombre: str
    correo: str
    id_cliente: str

    def __repr__(self) -> str:
        return f"Cliente(id={self.id_cliente!r}, nombre={self.nombre!r}, correo={self.correo!r})"
