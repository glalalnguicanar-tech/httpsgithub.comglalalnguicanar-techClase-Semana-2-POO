import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.producto import Producto


class MainView:
	FONDO = "#edf2ee"
	PANEL = "#fffdf8"
	VERDE = "#176b5b"

	def __init__(self, root, servicio, on_logout, usuario_actual):
		self.root = root
		self.servicio = servicio
		self.on_logout = on_logout
		self.usuario_actual = usuario_actual
		self.usuario_seleccionado_id = None
		self.asset_dir = Path(__file__).resolve().parents[1] / "assets"
		self.logo_image = tk.BitmapImage(file=str(self.asset_dir / "restaurante_logo.xbm"), foreground="#f8d8a8", background=self.VERDE)
		self.ventas_image = tk.BitmapImage(file=str(self.asset_dir / "ventas_icon.xbm"), foreground=self.VERDE, background=self.PANEL)
		self.frame = tk.Frame(root, bg=self.FONDO)
		self.frame.pack(fill="both", expand=True)

		header = tk.Frame(self.frame, bg=self.VERDE, padx=20, pady=14)
		header.pack(fill="x")
		tk.Label(header, image=self.logo_image, text="SABOR LOCAL", compound="left", padx=8,
				 foreground="#f8d8a8", background=self.VERDE, font=("Arial", 11, "bold")).pack(side="left")
		tk.Label(header, text="|  Panel del restaurante", foreground="white", background=self.VERDE,
				 font=("Arial", 17, "bold")).pack(side="left", padx=(8, 0))
		self.usuario_sesion = tk.Label(header, text="", foreground="white", background=self.VERDE, font=("Arial", 10))
		self.usuario_sesion.pack(side="right", padx=(12, 0))
		tk.Button(header, text="Cerrar sesión", command=self.cerrar_sesion).pack(side="right")

		content = tk.Frame(self.frame, padx=18, pady=18, bg=self.FONDO)
		content.pack(fill="both", expand=True)
		self.notebook = ttk.Notebook(content)
		self.notebook.pack(fill="both", expand=True)
		self.tab_usuarios = tk.Frame(self.notebook, bg=self.PANEL)
		self.tab_productos = tk.Frame(self.notebook, bg=self.PANEL)
		self.tab_ventas = tk.Frame(self.notebook, bg=self.PANEL)
		self.notebook.add(self.tab_usuarios, text="Usuarios")
		self.notebook.add(self.tab_productos, text="Productos")
		self.notebook.add(self.tab_ventas, text="Ventas")
		self._configurar_tab_usuarios()
		self._configurar_tab_productos()
		self._configurar_tab_ventas()
		self.root.bind_all("<Return>", self._evento_tecla_return, add="+")
		self.root.bind_all("<Escape>", self._evento_tecla_escape, add="+")
		self.mostrar_usuarios()
		self.mostrar(usuario_actual)

	def mostrar(self, usuario_actual=None):
		if usuario_actual is not None:
			self.usuario_actual = usuario_actual
		self.usuario_sesion.config(text=f"{self.usuario_actual.nombre} · {self.usuario_actual.rol}")
		if self.usuario_actual.rol == "Administrador":
			self.notebook.tab(self.tab_usuarios, state="normal")
			self.mostrar_usuarios()
		else:
			self.notebook.tab(self.tab_usuarios, state="hidden")
			self.notebook.select(self.tab_productos)
		self.frame.pack(fill="both", expand=True)

	def _configurar_tab_usuarios(self):
		tk.Label(self.tab_usuarios, text="Gestión de usuarios", font=("Arial", 15, "bold"),
				 background=self.PANEL, foreground="#18352f").pack(anchor="w", padx=18, pady=(15, 2))
		tk.Label(self.tab_usuarios, text="Seleccione una fila para consultar y editar una cuenta.",
				 background=self.PANEL, foreground="#52645d").pack(anchor="w", padx=18, pady=(0, 12))

		form = tk.Frame(self.tab_usuarios, bg=self.PANEL)
		form.pack(fill="x", padx=18, pady=(0, 12))
		self.campos_usuario = {}
		for columna, (titulo, clave) in enumerate((("Nombre", "nombre"), ("Usuario", "nombre_usuario"), ("Contraseña", "contrasena"))):
			tk.Label(form, text=titulo, bg=self.PANEL, font=("Arial", 10, "bold")).grid(row=0, column=columna, sticky="w", padx=(0, 12))
			campo = tk.Entry(form, show="*" if clave == "contrasena" else "", width=24)
			campo.grid(row=1, column=columna, sticky="ew", padx=(0, 12), pady=(4, 0))
			self.campos_usuario[clave] = campo
			campo.bind("<Escape>", self._evento_tecla_escape, add="+")
			campo.bind("<Return>", self._evento_tecla_return, add="+")
		form.columnconfigure((0, 1, 2), weight=1)
		self.campos_usuario["contrasena"].config(show="*")
		tk.Label(form, text="Rol", bg=self.PANEL, font=("Arial", 10, "bold")).grid(row=0, column=3, sticky="w", padx=(0, 12))
		self.rol_usuario = ttk.Combobox(form, state="readonly", values=("Empleado", "Cliente"), width=18)
		self.rol_usuario.set("Empleado")
		self.rol_usuario.grid(row=1, column=3, sticky="ew", padx=(0, 12), pady=(4, 0))
		self.rol_usuario.bind("<<ComboboxSelected>>", self._evento_cambio_rol)
		self.rol_usuario.bind("<Return>", self._evento_tecla_return, add="+")
		self.rol_usuario.bind("<Escape>", self._evento_tecla_escape, add="+")
		self.estado_usuarios = tk.Label(form, text="", bg=self.PANEL, fg=self.VERDE, anchor="w")
		self.estado_usuarios.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(8, 0))

		acciones = tk.Frame(self.tab_usuarios, bg=self.PANEL)
		acciones.pack(fill="x", padx=18, pady=(0, 12))
		for texto, accion in (("Registrar", self.registrar_usuario), ("Actualizar", self.actualizar_usuario),
							 ("Eliminar", self.eliminar_usuario), ("Limpiar", self.limpiar_formulario_usuario)):
			tk.Button(acciones, text=texto, command=accion).pack(side="left", padx=(0, 8))

		contenedor_tabla = tk.Frame(self.tab_usuarios, bg=self.PANEL)
		contenedor_tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		columnas = ("id", "nombre", "nombre_usuario", "rol")
		self.tree_usuarios = ttk.Treeview(contenedor_tabla, columns=columnas, show="headings", height=11, selectmode="browse")
		for columna, titulo, ancho in (("id", "ID", 65), ("nombre", "Nombre", 240), ("nombre_usuario", "Usuario", 190), ("rol", "Rol", 140)):
			self.tree_usuarios.heading(columna, text=titulo)
			self.tree_usuarios.column(columna, width=ancho, anchor="center" if columna in ("id", "rol") else "w")
		barra = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=self.tree_usuarios.yview)
		self.tree_usuarios.configure(yscrollcommand=barra.set)
		self.tree_usuarios.pack(side="left", fill="both", expand=True)
		barra.pack(side="right", fill="y")
		self.tree_usuarios.bind("<<TreeviewSelect>>", self._evento_seleccion_usuario)
		self.tree_usuarios.bind("<Escape>", self._evento_tecla_escape, add="+")

	def _configurar_tab_productos(self):
		form = tk.Frame(self.tab_productos, bg=self.PANEL)
		form.pack(fill="x", padx=18, pady=(16, 12))
		self.entradas = {}
		for fila, (titulo, clave) in enumerate((("Código", "codigo"), ("Nombre", "nombre"), ("Categoría", "categoria"), ("Precio", "precio"), ("Cantidad", "cantidad"))):
			tk.Label(form, text=titulo, bg=self.PANEL, font=("Arial", 10, "bold")).grid(row=fila, column=0, padx=(0, 12), pady=5, sticky="w")
			entrada = tk.Entry(form, width=26)
			entrada.grid(row=fila, column=1, padx=(0, 18), pady=5, sticky="w")
			self.entradas[clave] = entrada
		botones = tk.Frame(form, bg=self.PANEL)
		botones.grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 0))
		for texto, accion in (("Registrar", self.registrar_producto), ("Consultar", self.consultar_producto),
							 ("Actualizar", self.actualizar_producto), ("Eliminar", self.eliminar_producto),
							 ("Limpiar", self.limpiar_formulario_producto)):
			tk.Button(botones, text=texto, command=accion).pack(side="left", padx=(0, 7))
		self.lista_productos = ttk.Treeview(self.tab_productos, columns=("codigo", "nombre", "categoria", "precio", "cantidad"), show="headings", height=12)
		for columna, titulo, ancho in (("codigo", "Código", 90), ("nombre", "Nombre", 220), ("categoria", "Categoría", 130), ("precio", "Precio", 110), ("cantidad", "Stock", 80)):
			self.lista_productos.heading(columna, text=titulo)
			self.lista_productos.column(columna, width=ancho, anchor="center")
		self.lista_productos.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		self.actualizar_tabla_productos()

	def _configurar_tab_ventas(self):
		tk.Label(self.tab_ventas, image=self.ventas_image, text="Registrar venta", compound="left", padx=5,
				 font=("Arial", 14, "bold"), bg=self.PANEL).pack(anchor="w", padx=18, pady=(15, 3))
		tk.Label(self.tab_ventas, text="Seleccione un usuario y un producto para guardar la operación.",
				 bg=self.PANEL, fg="#475569").pack(anchor="w", padx=18, pady=(0, 12))
		formulario = tk.Frame(self.tab_ventas, bg=self.PANEL)
		formulario.pack(fill="x", padx=18, pady=(0, 16))
		tk.Label(formulario, text="Usuario", bg=self.PANEL, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=(0, 8), pady=5)
		self.usuario_venta = ttk.Combobox(formulario, state="readonly", width=26)
		self.usuario_venta.grid(row=0, column=1, padx=(0, 18), pady=5)
		tk.Label(formulario, text="Producto", bg=self.PANEL, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=(0, 8), pady=5)
		self.producto_venta = ttk.Combobox(formulario, state="readonly", width=32)
		self.producto_venta.grid(row=0, column=3, padx=(0, 18), pady=5)
		tk.Button(formulario, text="Registrar venta", command=self.registrar_venta).grid(row=0, column=4, pady=5)
		self.tabla_ventas = ttk.Treeview(self.tab_ventas, columns=("usuario", "producto", "fecha"), show="headings", height=12)
		for columna, titulo, ancho in (("usuario", "Usuario", 180), ("producto", "Producto", 280), ("fecha", "Fecha", 180)):
			self.tabla_ventas.heading(columna, text=titulo)
			self.tabla_ventas.column(columna, width=ancho, anchor="center")
		self.tabla_ventas.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		self.actualizar_controles_venta()
		self.actualizar_tabla_ventas()

	def _mostrar_mensaje(self, mensaje, tipo="info"):
		if tipo == "error":
			messagebox.showerror("Restaurante App", mensaje, parent=self.root)
		elif tipo == "confirmacion":
			return messagebox.askyesno("Restaurante App", mensaje, parent=self.root)
		else:
			messagebox.showinfo("Restaurante App", mensaje, parent=self.root)

	def _datos_usuario_formulario(self):
		return {clave: entrada.get().strip() for clave, entrada in self.campos_usuario.items()}

	def _evento_seleccion_usuario(self, event):
		seleccion = self.tree_usuarios.selection()
		if not seleccion:
			return
		self.usuario_seleccionado_id = int(seleccion[0])
		try:
			usuario = self.servicio.buscar_usuario_por_id(self.usuario_seleccionado_id, self.usuario_actual)
			if usuario is None:
				self.limpiar_formulario_usuario()
				return
			self.campos_usuario["nombre"].delete(0, tk.END)
			self.campos_usuario["nombre"].insert(0, usuario.nombre)
			self.campos_usuario["nombre_usuario"].delete(0, tk.END)
			self.campos_usuario["nombre_usuario"].insert(0, usuario.nombre_usuario)
			self.campos_usuario["contrasena"].delete(0, tk.END)
			self.rol_usuario["values"] = ("Empleado", "Cliente", "Administrador") if usuario.rol == "Administrador" else ("Empleado", "Cliente")
			self.rol_usuario.set(usuario.rol)
			self.estado_usuarios.config(text=f"Cuenta {usuario.id} consultada; la contraseña no se muestra.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def _evento_cambio_rol(self, event):
		self.estado_usuarios.config(text=f"Rol seleccionado para la cuenta: {self.rol_usuario.get()}.")

	def _evento_tecla_return(self, event):
		if event.widget in (*self.campos_usuario.values(), self.rol_usuario):
			self.registrar_usuario()
			return "break"

	def _evento_tecla_escape(self, event):
		widget = event.widget
		while widget is not None:
			if widget == self.tab_usuarios:
				self.limpiar_formulario_usuario()
				return "break"
			widget = getattr(widget, "master", None)

	def registrar_usuario(self):
		try:
			datos = self._datos_usuario_formulario()
			usuario = self.servicio.registrar_usuario(datos["nombre"], datos["nombre_usuario"], datos["contrasena"], self.rol_usuario.get(), self.usuario_actual)
			self.mostrar_usuarios()
			self.actualizar_controles_venta()
			self.limpiar_formulario_usuario()
			self._mostrar_mensaje(f"Cuenta {usuario.nombre_usuario} registrada correctamente como {usuario.rol}.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def actualizar_usuario(self):
		if self.usuario_seleccionado_id is None:
			self._mostrar_mensaje("Seleccione una cuenta en la tabla antes de actualizarla.", "error")
			return
		try:
			datos = self._datos_usuario_formulario()
			usuario = self.servicio.actualizar_usuario(self.usuario_seleccionado_id, datos["nombre"], datos["nombre_usuario"], datos["contrasena"], self.rol_usuario.get(), self.usuario_actual)
			self.mostrar_usuarios()
			self.actualizar_controles_venta()
			self.limpiar_formulario_usuario()
			self._mostrar_mensaje(f"Cuenta {usuario.nombre_usuario} actualizada correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def eliminar_usuario(self):
		if self.usuario_seleccionado_id is None:
			self._mostrar_mensaje("Seleccione una cuenta en la tabla antes de eliminarla.", "error")
			return
		usuario = self.servicio.buscar_usuario_por_id(self.usuario_seleccionado_id, self.usuario_actual)
		if usuario is None:
			self._mostrar_mensaje("La cuenta seleccionada ya no está disponible.", "error")
			return
		if not self._mostrar_mensaje(f"¿Desea eliminar la cuenta {usuario.nombre_usuario}?", "confirmacion"):
			return
		try:
			if not self.servicio.eliminar_usuario(usuario.id, self.usuario_actual):
				self._mostrar_mensaje("No se encontró la cuenta seleccionada.", "error")
				return
			self.mostrar_usuarios()
			self.actualizar_controles_venta()
			self.limpiar_formulario_usuario()
			self._mostrar_mensaje(f"Cuenta {usuario.nombre_usuario} eliminada correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def limpiar_formulario_usuario(self):
		for entrada in self.campos_usuario.values():
			entrada.delete(0, tk.END)
		self.rol_usuario["values"] = ("Empleado", "Cliente")
		self.rol_usuario.set("Empleado")
		self.usuario_seleccionado_id = None
		seleccion = self.tree_usuarios.selection()
		if seleccion:
			self.tree_usuarios.selection_remove(*seleccion)
		self.estado_usuarios.config(text="Formulario listo para una nueva cuenta.")

	def mostrar_usuarios(self):
		self.tree_usuarios.delete(*self.tree_usuarios.get_children())
		for usuario in self.servicio.listar_usuarios():
			self.tree_usuarios.insert("", tk.END, iid=str(usuario.id), values=(usuario.id, usuario.nombre, usuario.nombre_usuario, usuario.rol))

	def _obtener_producto_desde_formulario(self):
		datos = {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}
		if not datos["codigo"] or not datos["nombre"]:
			raise ValueError("El código y el nombre del producto son obligatorios.")
		return {"codigo": datos["codigo"], "nombre": datos["nombre"], "categoria": datos["categoria"] or "general", "precio": float(datos["precio"] or 0), "cantidad": int(datos["cantidad"] or 0)}

	def limpiar_formulario_producto(self):
		for entrada in self.entradas.values():
			entrada.delete(0, tk.END)

	def registrar_producto(self):
		try:
			self.servicio.registrar_producto(Producto(**self._obtener_producto_desde_formulario()))
			self.limpiar_formulario_producto()
			self.actualizar_tabla_productos()
			self.actualizar_controles_venta()
			self._mostrar_mensaje("Producto registrado correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def consultar_producto(self):
		producto = self.servicio.buscar_producto_por_codigo(self.entradas["codigo"].get().strip())
		if producto is None:
			self._mostrar_mensaje("No existe un producto con ese código.", "error")
			return
		for clave, valor in (("nombre", producto.nombre), ("categoria", producto.categoria), ("precio", producto.precio), ("cantidad", producto.cantidad)):
			self.entradas[clave].delete(0, tk.END)
			self.entradas[clave].insert(0, str(valor))

	def actualizar_producto(self):
		try:
			self.servicio.actualizar_producto(self.entradas["codigo"].get().strip(), self.entradas["nombre"].get().strip() or None, self.entradas["categoria"].get().strip() or None, self.entradas["precio"].get().strip() or None, self.entradas["cantidad"].get().strip() or None)
			self.actualizar_tabla_productos()
			self.actualizar_controles_venta()
			self._mostrar_mensaje("Producto actualizado correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def eliminar_producto(self):
		try:
			if not self.servicio.eliminar_producto(self.entradas["codigo"].get().strip()):
				raise ValueError("No existe un producto con ese código.")
			self.limpiar_formulario_producto()
			self.actualizar_tabla_productos()
			self.actualizar_controles_venta()
			self._mostrar_mensaje("Producto eliminado correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def actualizar_tabla_productos(self):
		self.lista_productos.delete(*self.lista_productos.get_children())
		for producto in self.servicio.listar_productos():
			self.lista_productos.insert("", tk.END, values=(producto.codigo, producto.nombre, producto.categoria, f"${producto.precio:.2f}", producto.cantidad))

	def actualizar_controles_venta(self):
		self.usuario_venta["values"] = [usuario.nombre_usuario for usuario in self.servicio.listar_usuarios()]
		self.producto_venta["values"] = [f"{producto.codigo} | {producto.nombre}" for producto in self.servicio.listar_productos()]
		if self.usuario_venta["values"] and not self.usuario_venta.get():
			self.usuario_venta.current(0)
		if self.producto_venta["values"] and not self.producto_venta.get():
			self.producto_venta.current(0)

	def registrar_venta(self):
		seleccion_producto = self.producto_venta.get()
		try:
			codigo_producto = seleccion_producto.split(" | ", 1)[0]
			venta = self.servicio.registrar_venta(self.usuario_venta.get(), codigo_producto)
			self.actualizar_tabla_ventas()
			self._mostrar_mensaje(f"Venta registrada: {venta.producto} para {venta.usuario}.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def actualizar_tabla_ventas(self):
		self.tabla_ventas.delete(*self.tabla_ventas.get_children())
		for venta in self.servicio.listar_ventas():
			self.tabla_ventas.insert("", tk.END, values=(venta.usuario, venta.producto, venta.fecha))

	def cerrar_sesion(self):
		self.frame.pack_forget()
		self.on_logout()
