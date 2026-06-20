class Cliente:
    """Clase que representa un cliente del restaurante."""
    
    def __init__(self, id, nombre, email, telefono, direccion):
        """
        Inicializa un cliente del restaurante.
        
        Args:
            id (int): Identificador único del cliente
            nombre (str): Nombre completo del cliente
            email (str): Correo electrónico del cliente
            telefono (str): Número de teléfono del cliente
            direccion (str): Dirección de entrega del cliente
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.historial_pedidos = []
        self.es_miembro_premium = False
    
    def __str__(self):
        """Retorna una representación en string del cliente."""
        return f"{self.nombre} - {self.email}"
    
    def __repr__(self):
        """Retorna una representación detallada del cliente."""
        return f"Cliente(id={self.id}, nombre='{self.nombre}', email='{self.email}')"
    
    def obtener_informacion(self):
        """Retorna la información completa del cliente."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'es_miembro_premium': self.es_miembro_premium,
            'cantidad_pedidos': len(self.historial_pedidos)
        }
    
    def agregar_pedido(self, pedido):
        """
        Agrega un pedido al historial del cliente.
        
        Args:
            pedido: Objeto de pedido a agregar al historial
        """
        self.historial_pedidos.append(pedido)
    
    def obtener_historial_pedidos(self):
        """Retorna el historial de pedidos del cliente."""
        return self.historial_pedidos
    
    def cambiar_membresia_premium(self, es_premium):
        """
        Cambia el estado de membresía premium del cliente.
        
        Args:
            es_premium (bool): True para activar, False para desactivar
        """
        self.es_miembro_premium = es_premium
    
    def obtener_total_gastado(self):
        """
        Calcula el monto total gastado por el cliente en todos sus pedidos.
        
        Returns:
            float: Total gastado
        """
        return sum(pedido.total for pedido in self.historial_pedidos if hasattr(pedido, 'total'))
    
    def actualizar_contacto(self, email=None, telefono=None, direccion=None):
        """
        Actualiza la información de contacto del cliente.
        
        Args:
            email (str): Nuevo correo electrónico (opcional)
            telefono (str): Nuevo número de teléfono (opcional)
            direccion (str): Nueva dirección (opcional)
        """
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono
        if direccion:
            self.direccion = direccion
