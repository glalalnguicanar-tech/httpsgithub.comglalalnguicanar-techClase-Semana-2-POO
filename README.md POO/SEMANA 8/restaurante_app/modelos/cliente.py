from dataclasses import dataclass

@dataclass
class Cliente:
    identificacion: str
    nombre: str
    correo: str

    def mostrar_informacion(self) -> str:
        return (
            f"Cliente [{self.identificacion}] - {self.nombre} | Correo: {self.correo}"
        )
