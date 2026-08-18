from __future__ import annotations


class Usuario:
    """Representa a una persona registrada en el sistema."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.correo = correo.strip()

    def __str__(self) -> str:
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"
