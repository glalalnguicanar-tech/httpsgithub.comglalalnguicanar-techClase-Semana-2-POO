from dataclasses import dataclass

@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float

    def mostrar_informacion(self) -> str:
        return (
            f"Producto [{self.codigo}] - {self.nombre} | Categoría: {self.categoria} "
            f"| Precio: ${self.precio:.2f}"
        )
