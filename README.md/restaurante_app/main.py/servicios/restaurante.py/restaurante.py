from datetime import datetime


class Pedido:
    """Clase que representa un pedido del restaurante."""
    
    def __init__(self, id, cliente, productos, fecha=None):
        """
        Inicializa un pedido.
        
        Args:
            id (int): Identificador único del pedido
            cliente: Objeto Cliente que realiza el pedido
            productos (list): Lista de tuplas (Producto, cantidad)
            fecha: Fecha del pedido (por defecto, la fecha y hora actual)
        """
        self.id = id
        self.cliente = cliente
        self.productos = productos
        self.fecha = fecha or datetime.now()
        self.estado = "pendiente"
        self.total = self._calcular_total()
    
    def _calcular_total(self):
        """Calcula el total del pedido."""
        total = 0
        for producto, cantidad in self.productos:
            total += producto.precio * cantidad
        return total
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del pedido."""
        self.estado = nuevo_estado
    
    def obtener_informacion(self):
        """Retorna la información del pedido."""
        return {
            'id': self.id,
            'cliente': self.cliente.nombre,
            'fecha': self.fecha,
            'estado': self.estado,
            'total': self.total,
            'cantidad_items': sum(cant for _, cant in self.productos)
        }


class Restaurante:
    """Clase que gestiona las operaciones principales del restaurante."""
    
    def __init__(self, nombre, direccion, telefono):
        """
        Inicializa un restaurante.
        
        Args:
            nombre (str): Nombre del restaurante
            direccion (str): Dirección del restaurante
            telefono (str): Teléfono de contacto del restaurante
        """
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.clientes = {}
        self.productos = {}
        self.pedidos = {}
        self.contador_clientes = 1
        self.contador_productos = 1
        self.contador_pedidos = 1
    
    def __str__(self):
        """Retorna la información del restaurante."""
        return f"{self.nombre} - {self.direccion}"
    
    # ========== Métodos para gestionar clientes ==========
    
    def registrar_cliente(self, nombre, email, telefono, direccion):
        """
        Registra un nuevo cliente en el restaurante.
        
        Args:
            nombre (str): Nombre del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente
            direccion (str): Dirección del cliente
            
        Returns:
            Cliente: El objeto del cliente creado
        """
        from modelos.cliente import Cliente
        
        cliente = Cliente(self.contador_clientes, nombre, email, telefono, direccion)
        self.clientes[self.contador_clientes] = cliente
        self.contador_clientes += 1
        return cliente
    
    def obtener_cliente(self, id_cliente):
        """
        Obtiene un cliente por su ID.
        
        Args:
            id_cliente (int): ID del cliente
            
        Returns:
            Cliente: El objeto del cliente o None si no existe
        """
        return self.clientes.get(id_cliente)
    
    def listar_clientes(self):
        """Retorna la lista de todos los clientes."""
        return list(self.clientes.values())
    
    def actualizar_cliente(self, id_cliente, email=None, telefono=None, direccion=None):
        """
        Actualiza la información de un cliente.
        
        Args:
            id_cliente (int): ID del cliente
            email (str): Nuevo email (opcional)
            telefono (str): Nuevo teléfono (opcional)
            direccion (str): Nueva dirección (opcional)
            
        Returns:
            bool: True si se actualiza, False si el cliente no existe
        """
        cliente = self.obtener_cliente(id_cliente)
        if cliente:
            cliente.actualizar_contacto(email, telefono, direccion)
            return True
        return False
    
    # ========== Métodos para gestionar productos ==========
    
    def agregar_producto(self, nombre, descripcion, precio, categoria):
        """
        Agrega un nuevo producto al menú del restaurante.
        
        Args:
            nombre (str): Nombre del producto
            descripcion (str): Descripción del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto
            
        Returns:
            Producto: El objeto del producto creado
        """
        from modelos.producto import Producto
        
        producto = Producto(self.contador_productos, nombre, descripcion, precio, categoria)
        self.productos[self.contador_productos] = producto
        self.contador_productos += 1
        return producto
    
    def obtener_producto(self, id_producto):
        """
        Obtiene un producto por su ID.
        
        Args:
            id_producto (int): ID del producto
            
        Returns:
            Producto: El objeto del producto o None si no existe
        """
        return self.productos.get(id_producto)
    
    def listar_productos(self, categoria=None):
        """
        Retorna la lista de productos, opcionalmente filtrados por categoría.
        
        Args:
            categoria (str): Filtrar por categoría (opcional)
            
        Returns:
            list: Lista de productos
        """
        if categoria:
            return [p for p in self.productos.values() if p.categoria == categoria]
        return list(self.productos.values())
    
    def actualizar_disponibilidad_producto(self, id_producto, disponible):
        """
        Actualiza la disponibilidad de un producto.
        
        Args:
            id_producto (int): ID del producto
            disponible (bool): Nuevo estado de disponibilidad
            
        Returns:
            bool: True si se actualiza, False si el producto no existe
        """
        producto = self.obtener_producto(id_producto)
        if producto:
            producto.cambiar_disponibilidad(disponible)
            return True
        return False
    
    # ========== Métodos para gestionar pedidos ==========
    
    def crear_pedido(self, id_cliente, items_pedido):
        """
        Crea un nuevo pedido para un cliente.
        
        Args:
            id_cliente (int): ID del cliente
            items_pedido (list): Lista de tuplas (id_producto, cantidad)
            
        Returns:
            Pedido: El objeto del pedido creado o None si hay error
        """
        cliente = self.obtener_cliente(id_cliente)
        if not cliente:
            return None
        
        productos = []
        for id_producto, cantidad in items_pedido:
            producto = self.obtener_producto(id_producto)
            if producto and producto.disponible:
                productos.append((producto, cantidad))
        
        if not productos:
            return None
        
        pedido = Pedido(self.contador_pedidos, cliente, productos)
        self.pedidos[self.contador_pedidos] = pedido
        cliente.agregar_pedido(pedido)
        self.contador_pedidos += 1
        return pedido
    
    def obtener_pedido(self, id_pedido):
        """
        Obtiene un pedido por su ID.
        
        Args:
            id_pedido (int): ID del pedido
            
        Returns:
            Pedido: El objeto del pedido o None si no existe
        """
        return self.pedidos.get(id_pedido)
    
    def listar_pedidos(self, estado=None):
        """
        Retorna la lista de pedidos, opcionalmente filtrados por estado.
        
        Args:
            estado (str): Filtrar por estado (opcional)
            
        Returns:
            list: Lista de pedidos
        """
        if estado:
            return [p for p in self.pedidos.values() if p.estado == estado]
        return list(self.pedidos.values())
    
    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        """
        Actualiza el estado de un pedido.
        
        Args:
            id_pedido (int): ID del pedido
            nuevo_estado (str): Nuevo estado del pedido
            
        Returns:
            bool: True si se actualiza, False si el pedido no existe
        """
        pedido = self.obtener_pedido(id_pedido)
        if pedido:
            pedido.cambiar_estado(nuevo_estado)
            return True
        return False
    
    # ========== Métodos de reportes y estadísticas ==========
    
    def obtener_informacion_restaurante(self):
        """Retorna información general del restaurante."""
        return {
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'total_clientes': len(self.clientes),
            'total_productos': len(self.productos),
            'total_pedidos': len(self.pedidos)
        }
    
    def obtener_ingresos_totales(self):
        """Calcula los ingresos totales del restaurante."""
        return sum(pedido.total for pedido in self.pedidos.values())
    
    def obtener_cliente_frecuente(self):
        """Retorna el cliente que ha realizado más pedidos."""
        if not self.pedidos:
            return None
        
        clientes_pedidos = {}
        for pedido in self.pedidos.values():
            id_cliente = pedido.cliente.id
            clientes_pedidos[id_cliente] = clientes_pedidos.get(id_cliente, 0) + 1
        
        id_cliente_frecuente = max(clientes_pedidos, key=clientes_pedidos.get)
        return self.obtener_cliente(id_cliente_frecuente)
    
    def generar_reporte(self):
        """Genera un reporte general del restaurante."""
        return {
            'informacion': self.obtener_informacion_restaurante(),
            'ingresos_totales': self.obtener_ingresos_totales(),
            'pedidos_pendientes': len(self.listar_pedidos('pendiente')),
            'cliente_frecuente': self.obtener_cliente_frecuente().nombre if self.obtener_cliente_frecuente() else None