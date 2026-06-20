class Producto:
    """Clase que representa un producto del restaurante."""
    
    def __init__(self, id, nombre, descripcion, precio, categoria, disponible=True):
        """
        Inicializa un producto del restaurante.
        
        Args:
            id (int): Identificador único del producto
            nombre (str): Nombre del producto
            descripcion (str): Descripción del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto (ej: "Plato Principal", "Bebida", "Postre")
            disponible (bool): Indica si el producto está disponible. Por defecto es True
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.disponible = disponible
    
    def __str__(self):
        """Retorna una representación en string del producto."""
        return f"{self.nombre} - ${self.precio} ({self.categoria})"
    
    def __repr__(self):
        """Retorna una representación detallada del producto."""
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio}, disponible={self.disponible})"
    
    def obtener_informacion(self):
        """Retorna la información completa del producto."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'categoria': self.categoria,
            'disponible': self.disponible
        }
    
    def cambiar_disponibilidad(self, disponible):
        """
        Cambia el estado de disponibilidad del producto.
        
        Args:
            disponible (bool): Nuevo estado de disponibilidad
        """
        self.disponible = disponible
    
    def aplicar_descuento(self, porcentaje):
        """
        Aplica un descuento al precio del producto.
        
        Args:
            porcentaje (float): Porcentaje de descuento a aplicar
            
        Returns:
            float: Precio con descuento aplicado
        """
        descuento = self.precio * (porcentaje / 100)
        return self.precio - descuento
