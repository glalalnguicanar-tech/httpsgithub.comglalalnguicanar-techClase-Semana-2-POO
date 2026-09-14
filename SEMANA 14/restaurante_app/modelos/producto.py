class Producto:
    def __init__(self, codigo=None, nombre="", categoria="general", precio=0, cantidad=0, **kwargs):
        codigo_raw = codigo if codigo is not None else kwargs.get("id", "")
        self.codigo = str(codigo_raw or kwargs.get("codigo", "") or kwargs.get("identificacion", "") or "").strip()
        self.nombre = str(nombre or kwargs.get("nombre", "")).strip()
        self.categoria = str(categoria or kwargs.get("categoria", "general")).strip() or "general"
        self.precio = float(precio)
        self.cantidad = int(cantidad)

        if not self.codigo:
            self.codigo = self.nombre.lower().replace(" ", "_") if self.nombre else "producto"
        self._validar()

    def _validar(self):
        if not self.codigo:
            raise ValueError("El código del producto es obligatorio.")
        if not self.nombre:
            raise ValueError("El nombre del producto es obligatorio.")
        if not self.categoria:
            raise ValueError("La categoría del producto es obligatoria.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }

    def __str__(self):
        return f"{self.codigo} | {self.nombre} | {self.categoria} | ${self.precio:.2f} | Stock: {self.cantidad}"
