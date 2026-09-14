from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
    def __init__(self, archivo_servicio, ruta_productos, ruta_usuarios):
        self.archivo_servicio = archivo_servicio
        self.ruta_productos = Path(ruta_productos)
        self.ruta_usuarios = Path(ruta_usuarios)
        self.productos = self._cargar_productos()
        self.usuarios = self._cargar_usuarios()

    def _cargar_productos(self):
        productos = []
        for datos in self.archivo_servicio.leer_json(self.ruta_productos):
            try:
                productos.append(Producto(**datos))
            except TypeError:
                productos.append(Producto(
                    codigo=datos.get("codigo", ""),
                    nombre=datos.get("nombre", ""),
                    categoria=datos.get("categoria", "general"),
                    precio=datos.get("precio", 0),
                    cantidad=datos.get("cantidad", 0),
                ))
            except ValueError:
                if "nombre" in datos:
                    productos.append(Producto(
                        codigo=datos.get("codigo") or datos.get("id") or datos.get("nombre", "").lower().replace(" ", "_"),
                        nombre=datos.get("nombre", ""),
                        categoria=datos.get("categoria", "general"),
                        precio=datos.get("precio", 0),
                        cantidad=datos.get("cantidad", 0),
                    ))
        return productos

    def _cargar_usuarios(self):
        usuarios = []
        for datos in self.archivo_servicio.leer_json(self.ruta_usuarios):
            usuarios.append(Usuario(**datos))
        return usuarios

    def _guardar_productos(self):
        self.archivo_servicio.guardar_json(
            self.ruta_productos,
            [producto.to_dict() for producto in self.productos],
        )

    def validar_acceso(self, nombre_usuario, contrasena):
        return any(
            usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena
            for usuario in self.usuarios
        )

    def listar_productos(self):
        return sorted(self.productos, key=lambda producto: producto.codigo.lower())

    def listar_usuarios(self):
        return list(self.usuarios)

    def consultar_cantidad_productos(self):
        return sum(producto.cantidad for producto in self.productos)

    def registrar_producto(self, producto):
        if self.buscar_producto_por_codigo(producto.codigo):
            raise ValueError("Ya existe un producto con ese código.")
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def buscar_producto_por_codigo(self, codigo):
        codigo_buscar = str(codigo).strip().lower()
        for producto in self.productos:
            if producto.codigo.lower() == codigo_buscar:
                return producto
        return None

    def actualizar_producto(self, codigo, nombre=None, categoria=None, precio=None, cantidad=None):
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")

        if nombre is not None:
            producto.nombre = str(nombre).strip()
        if categoria is not None:
            producto.categoria = str(categoria).strip() or "general"
        if precio is not None:
            producto.precio = float(precio)
        if cantidad is not None:
            producto.cantidad = int(cantidad)

        producto._validar()
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        self._guardar_productos()
        return True
