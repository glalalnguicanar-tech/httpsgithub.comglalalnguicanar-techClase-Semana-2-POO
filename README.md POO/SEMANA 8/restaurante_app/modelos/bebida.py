from .producto import Producto

class Bebida(Producto):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        tamano: str,
        envase: str,
    ) -> None:
        super().__init__(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)
        self.tamano = tamano
        self.envase = envase

    def mostrar_informacion(self) -> str:
        informacion_base = super().mostrar_informacion()
        return (
            f"{informacion_base} | Tamaño: {self.tamano} | Envase: {self.envase}"
        )
