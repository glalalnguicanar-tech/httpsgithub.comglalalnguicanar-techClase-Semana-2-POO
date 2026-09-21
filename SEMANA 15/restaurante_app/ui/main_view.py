import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.producto import Producto


class MainView:
	def __init__(self, root, servicio, on_logout):
		self.root = root
		self.servicio = servicio
		self.on_logout = on_logout
		self.logo_asset = Path(__file__).resolve().parents[1] / "assets" / "restaurante_logo.svg"
		self.ventas_asset = Path(__file__).resolve().parents[1] / "assets" / "ventas_icon.svg"
		self.logo_image = tk.BitmapImage(file=str(self.logo_asset.with_suffix(".xbm")), foreground="#f8d8a8", background="#176b5b")
		self.ventas_image = tk.BitmapImage(file=str(self.ventas_asset.with_suffix(".xbm")), foreground="#176b5b", background="#fffdf8")
		self.frame = tk.Frame(root, bg="#eef4f1")
		self.frame.pack(fill="both", expand=True)

		header = tk.Frame(self.frame, bg="#176b5b", padx=20, pady=14)
		header.pack(fill="x")
		marca = "SABOR LOCAL" if self.logo_asset.exists() else "RESTAURANTE"
		tk.Label(header, image=self.logo_image, text=marca, compound="left", padx=8, fg="#f8d8a8", bg="#176b5b", font=("Arial", 11, "bold")).pack(side="left")
		tk.Label(header, text="  |  Panel principal", fg="white", bg="#176b5b", font=("Arial", 17, "bold")).pack(side="left")
		tk.Button(header, text="Cerrar sesión", command=self.cerrar_sesion, bg="#b42318", fg="white", relief="flat", padx=10).pack(side="right")

		content = tk.Frame(self.frame, padx=18, pady=18, bg="#eef4f1")
		content.pack(fill="both", expand=True)
		self.notebook = ttk.Notebook(content)
		self.notebook.pack(fill="both", expand=True)
		self.tab_usuarios = tk.Frame(self.notebook, bg="#fffdf8")
		self.tab_productos = tk.Frame(self.notebook, bg="#fffdf8")
		self.tab_ventas = tk.Frame(self.notebook, bg="#fffdf8")
		self.notebook.add(self.tab_usuarios, text="Usuarios")
		self.notebook.add(self.tab_productos, text="Productos")
		self.notebook.add(self.tab_ventas, text="Ventas")
		self._configurar_tab_usuarios()
		self._configurar_tab_productos()
		self._configurar_tab_ventas()
		self.mostrar_usuarios()

	def mostrar(self):
		self.frame.pack(fill="both", expand=True)

	def _configurar_tab_usuarios(self):
		tk.Label(self.tab_usuarios, text="Usuarios registrados", font=("Arial", 14, "bold"), bg="#fffdf8").pack(anchor="w", padx=18, pady=(15, 8))
		self.tree_usuarios = ttk.Treeview(self.tab_usuarios, columns=("usuario", "rol"), show="headings", height=14)
		for columna, titulo, ancho in (("usuario", "Usuario", 220), ("rol", "Rol", 140)):
			self.tree_usuarios.heading(columna, text=titulo)
			self.tree_usuarios.column(columna, width=ancho, anchor="center")
		self.tree_usuarios.pack(fill="both", expand=True, padx=18, pady=(0, 18))

	def _configurar_tab_productos(self):
		form = tk.Frame(self.tab_productos, bg="#fffdf8")
		form.pack(fill="x", padx=18, pady=(16, 12))
		self.entradas = {}
		for fila, (titulo, clave) in enumerate((("Código", "codigo"), ("Nombre", "nombre"), ("Categoría", "categoria"), ("Precio", "precio"), ("Cantidad", "cantidad"))):
			tk.Label(form, text=titulo, bg="#fffdf8", font=("Arial", 10, "bold")).grid(row=fila, column=0, padx=(0, 12), pady=5, sticky="w")
			entrada = tk.Entry(form, width=26)
			entrada.grid(row=fila, column=1, padx=(0, 18), pady=5, sticky="w")
			self.entradas[clave] = entrada
		botones = tk.Frame(form, bg="#fffdf8")
		botones.grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 0))
		for texto, accion, color in (("Registrar", self.registrar_producto, "#176b5b"), ("Consultar", self.consultar_producto, "#2563eb"), ("Actualizar", self.actualizar_producto, "#b45309"), ("Eliminar", self.eliminar_producto, "#b42318"), ("Limpiar", self.limpiar_formulario, "#64748b")):
			tk.Button(botones, text=texto, command=accion, bg=color, fg="white", relief="flat", padx=8).pack(side="left", padx=(0, 7))
		self.lista_productos = ttk.Treeview(self.tab_productos, columns=("codigo", "nombre", "categoria", "precio", "cantidad"), show="headings", height=12)
		for columna, titulo, ancho in (("codigo", "Código", 90), ("nombre", "Nombre", 220), ("categoria", "Categoría", 130), ("precio", "Precio", 110), ("cantidad", "Stock", 80)):
			self.lista_productos.heading(columna, text=titulo)
			self.lista_productos.column(columna, width=ancho, anchor="center")
		self.lista_productos.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		self.actualizar_tabla_productos()

	def _configurar_tab_ventas(self):
		titulo_ventas = "Registrar venta" if self.ventas_asset.exists() else "Registro de operación"
		tk.Label(self.tab_ventas, image=self.ventas_image, text=titulo_ventas, compound="left", padx=5, font=("Arial", 14, "bold"), bg="#fffdf8").pack(anchor="w", padx=18, pady=(15, 3))
		tk.Label(self.tab_ventas, text="Seleccione un usuario y un producto para guardar la operación.", bg="#fffdf8", fg="#475569").pack(anchor="w", padx=18, pady=(0, 12))
		formulario = tk.Frame(self.tab_ventas, bg="#fffdf8")
		formulario.pack(fill="x", padx=18, pady=(0, 16))
		tk.Label(formulario, text="Usuario", bg="#fffdf8", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=(0, 8), pady=5)
		self.usuario_venta = ttk.Combobox(formulario, state="readonly", width=26)
		self.usuario_venta.grid(row=0, column=1, padx=(0, 18), pady=5)
		tk.Label(formulario, text="Producto", bg="#fffdf8", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=(0, 8), pady=5)
		self.producto_venta = ttk.Combobox(formulario, state="readonly", width=32)
		self.producto_venta.grid(row=0, column=3, padx=(0, 18), pady=5)
		tk.Button(formulario, text="Registrar venta", command=self.registrar_venta, bg="#176b5b", fg="white", relief="flat", padx=12).grid(row=0, column=4, pady=5)
		self.tabla_ventas = ttk.Treeview(self.tab_ventas, columns=("usuario", "producto", "fecha"), show="headings", height=12)
		for columna, titulo, ancho in (("usuario", "Usuario", 180), ("producto", "Producto", 280), ("fecha", "Fecha", 180)):
			self.tabla_ventas.heading(columna, text=titulo)
			self.tabla_ventas.column(columna, width=ancho, anchor="center")
		self.tabla_ventas.pack(fill="both", expand=True, padx=18, pady=(0, 18))
		self.actualizar_controles_venta()
		self.actualizar_tabla_ventas()

	def _mostrar_mensaje(self, mensaje, tipo="info"):
		(messagebox.showerror if tipo == "error" else messagebox.showinfo)("Restaurante App", mensaje)

	def limpiar_formulario(self):
		for entrada in self.entradas.values():
			entrada.delete(0, tk.END)

	def _obtener_producto_desde_formulario(self):
		datos = {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}
		if not datos["codigo"] or not datos["nombre"]:
			raise ValueError("El código y el nombre del producto son obligatorios.")
		return {"codigo": datos["codigo"], "nombre": datos["nombre"], "categoria": datos["categoria"] or "general", "precio": float(datos["precio"] or 0), "cantidad": int(datos["cantidad"] or 0)}

	def registrar_producto(self):
		try:
			self.servicio.registrar_producto(Producto(**self._obtener_producto_desde_formulario()))
			self.limpiar_formulario()
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
			self.limpiar_formulario()
			self.actualizar_tabla_productos()
			self.actualizar_controles_venta()
			self._mostrar_mensaje("Producto eliminado correctamente.")
		except Exception as exc:
			self._mostrar_mensaje(str(exc), "error")

	def actualizar_tabla_productos(self):
		self.lista_productos.delete(*self.lista_productos.get_children())
		for producto in self.servicio.listar_productos():
			self.lista_productos.insert("", tk.END, values=(producto.codigo, producto.nombre, producto.categoria, f"${producto.precio:.2f}", producto.cantidad))

	def mostrar_usuarios(self):
		self.tree_usuarios.delete(*self.tree_usuarios.get_children())
		for usuario in self.servicio.listar_usuarios():
			self.tree_usuarios.insert("", tk.END, values=(usuario.nombre_usuario, usuario.rol))

	def actualizar_controles_venta(self):
		self.usuario_venta["values"] = [u.nombre_usuario for u in self.servicio.listar_usuarios()]
		self.producto_venta["values"] = [f"{p.codigo} | {p.nombre}" for p in self.servicio.listar_productos()]
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
