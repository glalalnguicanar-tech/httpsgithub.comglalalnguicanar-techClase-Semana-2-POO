from datetime import datetime
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
	def __init__(self, archivo_servicio, ruta_productos, ruta_usuarios, ruta_ventas):
		self.archivo_servicio = archivo_servicio
		self.ruta_productos = Path(ruta_productos)
		self.ruta_usuarios = Path(ruta_usuarios)
		self.ruta_ventas = Path(ruta_ventas)
		self.productos = self._cargar_productos()
		self.usuarios = self._cargar_usuarios()
		self.ventas = self._cargar_ventas()

	def _cargar_productos(self):
		productos = []
		for datos in self.archivo_servicio.leer_json(self.ruta_productos):
			try:
				productos.append(Producto(**datos))
			except (TypeError, ValueError):
				continue
		return productos

	def _cargar_usuarios(self):
		usuarios = []
		ids = set()
		datos_guardados = self.archivo_servicio.leer_json(self.ruta_usuarios)
		for datos in datos_guardados:
			try:
				usuario = Usuario(**datos)
				if usuario.id is None or usuario.id in ids:
					usuario.id = max(ids, default=0) + 1
				ids.add(usuario.id)
				usuarios.append(usuario)
			except (TypeError, ValueError):
				continue
		if usuarios and [usuario.to_dict() for usuario in usuarios] != datos_guardados:
			self._guardar_usuarios(usuarios)
		return usuarios

	def _cargar_ventas(self):
		ventas = []
		for datos in self.archivo_servicio.leer_json(self.ruta_ventas):
			try:
				ventas.append(Venta(**datos))
			except (TypeError, ValueError):
				continue
		return ventas

	def _guardar_productos(self):
		self.archivo_servicio.guardar_json(self.ruta_productos, [producto.to_dict() for producto in self.productos])

	def _guardar_usuarios(self, usuarios=None):
		usuarios = self.usuarios if usuarios is None else usuarios
		self.archivo_servicio.guardar_json(self.ruta_usuarios, [usuario.to_dict() for usuario in usuarios])

	def _guardar_ventas(self):
		self.archivo_servicio.guardar_json(self.ruta_ventas, [venta.to_dict() for venta in self.ventas])

	def autenticar(self, nombre_usuario, contrasena):
		return next((usuario for usuario in self.usuarios if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena), None)

	def validar_acceso(self, nombre_usuario, contrasena):
		return self.autenticar(nombre_usuario, contrasena) is not None

	def listar_productos(self):
		return sorted(self.productos, key=lambda producto: producto.codigo.casefold())

	def listar_usuarios(self):
		return list(self.usuarios)

	def listar_ventas(self):
		return list(self.ventas)

	def consultar_cantidad_productos(self):
		return sum(producto.cantidad for producto in self.productos)

	def _exigir_administrador(self, actor):
		if actor is None or actor.rol != "Administrador":
			raise PermissionError("Solo un administrador puede gestionar usuarios.")

	def _validar_usuario_unico(self, nombre_usuario, ignorar_id=None):
		if any(usuario.nombre_usuario.casefold() == nombre_usuario.casefold() and usuario.id != ignorar_id for usuario in self.usuarios):
			raise ValueError("Ya existe una cuenta con ese nombre de usuario.")

	def buscar_usuario_por_id(self, identificador, actor):
		self._exigir_administrador(actor)
		try:
			identificador = int(identificador)
		except (TypeError, ValueError):
			return None
		return next((usuario for usuario in self.usuarios if usuario.id == identificador), None)

	def registrar_usuario(self, nombre, nombre_usuario, contrasena, rol, actor):
		self._exigir_administrador(actor)
		rol = str(rol).strip()
		if rol not in ("Empleado", "Cliente"):
			raise ValueError("Los usuarios nuevos deben tener rol Empleado o Cliente.")
		nombre = str(nombre).strip()
		nombre_usuario = str(nombre_usuario).strip()
		contrasena = str(contrasena).strip()
		if not nombre or not nombre_usuario or not contrasena:
			raise ValueError("Complete nombre, usuario y contraseña.")
		self._validar_usuario_unico(nombre_usuario)
		usuario = Usuario(id=max((actual.id for actual in self.usuarios), default=0) + 1,
						  nombre=nombre, nombre_usuario=nombre_usuario, contrasena=contrasena, rol=rol)
		self.usuarios.append(usuario)
		self._guardar_usuarios()
		return usuario

	def actualizar_usuario(self, identificador, nombre, nombre_usuario, contrasena, rol, actor):
		self._exigir_administrador(actor)
		usuario = self.buscar_usuario_por_id(identificador, actor)
		if usuario is None:
			raise ValueError("Seleccione un usuario registrado.")
		if usuario.rol == "Administrador":
			raise ValueError("La gestión administrativa solo permite modificar Empleados y Clientes.")
		rol = str(rol).strip()
		if rol not in ("Empleado", "Cliente"):
			raise ValueError("Seleccione el rol Empleado o Cliente.")
		nombre = str(nombre).strip()
		nombre_usuario = str(nombre_usuario).strip()
		if not nombre or not nombre_usuario:
			raise ValueError("El nombre y el usuario son obligatorios.")
		self._validar_usuario_unico(nombre_usuario, usuario.id)
		usuario.nombre = nombre
		usuario.nombre_usuario = nombre_usuario
		usuario.rol = rol
		if str(contrasena).strip():
			usuario.contrasena = str(contrasena).strip()
		self._guardar_usuarios()
		return usuario

	def eliminar_usuario(self, identificador, actor):
		self._exigir_administrador(actor)
		usuario = self.buscar_usuario_por_id(identificador, actor)
		if usuario is None:
			return False
		if usuario.id == actor.id:
			raise ValueError("No puede eliminar la cuenta administrativa actualmente autenticada.")
		if usuario.rol == "Administrador":
			raise ValueError("Solo se pueden eliminar usuarios Empleados o Clientes.")
		self.usuarios.remove(usuario)
		self._guardar_usuarios()
		return True

	def registrar_producto(self, producto):
		if self.buscar_producto_por_codigo(producto.codigo):
			raise ValueError("Ya existe un producto con ese código.")
		self.productos.append(producto)
		self._guardar_productos()
		return producto

	def buscar_producto_por_codigo(self, codigo):
		codigo_buscar = str(codigo).strip().casefold()
		return next((producto for producto in self.productos if producto.codigo.casefold() == codigo_buscar), None)

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

	def registrar_venta(self, nombre_usuario, codigo_producto):
		usuario = next((actual for actual in self.usuarios if actual.nombre_usuario == nombre_usuario), None)
		producto = self.buscar_producto_por_codigo(codigo_producto)
		if usuario is None:
			raise ValueError("Seleccione un usuario registrado.")
		if producto is None:
			raise ValueError("Seleccione un producto registrado.")
		if producto.cantidad <= 0:
			raise ValueError("El producto seleccionado no tiene existencias.")
		venta = Venta(usuario.nombre_usuario, producto.nombre, datetime.now().strftime("%Y-%m-%d %H:%M"))
		self.ventas.append(venta)
		self._guardar_ventas()
		return venta
