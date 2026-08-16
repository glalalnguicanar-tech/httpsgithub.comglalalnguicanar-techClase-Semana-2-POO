class Producto:
    def __init__(self, nombre: str, precio: float, categoria: str, stock: int = 0, disponible: bool = True):
        self.nombre: str = nombre
        self.precio: float = precio
        self.categoria: str = categoria
        self.stock: int = stock
        self.disponible: bool = disponible

    def __repr__(self) -> str:
        return (
            f"Producto(nombre={self.nombre!r}, precio={self.precio}, "
            f"categoria={self.categoria!r}, stock={self.stock}, disponible={self.disponible})"
        )
