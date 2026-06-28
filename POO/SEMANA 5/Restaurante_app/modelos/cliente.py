class Cliente:
    def __init__(self, nombre: str, apellido: str, telefono: str, direccion: str, correo_electronico: str):
        self.nombre: str = nombre
        self.apellido: str = apellido
        self.telefono: str = telefono
        self.direccion: str = direccion
        self.correo_electronico: str = correo_electronico

    def __repr__(self) -> str:
        return (
            f"Cliente(nombre={self.nombre!r}, apellido={self.apellido!r}, "
            f"telefono={self.telefono!r}, direccion={self.direccion!r}, "
            f"correo_electronico={self.correo_electronico!r})"
        )
