import tkinter as tk
from tkinter import messagebox, ttk


class MainView:
    def __init__(self, root, servicio, on_logout):
        self.root = root
        self.servicio = servicio
        self.on_logout = on_logout

        self.frame = tk.Frame(root, bg="#eef2f6")
        self.frame.pack(fill="both", expand=True)

        header = tk.Frame(self.frame, bg="#1f2937", padx=20, pady=16)
        header.pack(fill="x")

        tk.Label(header, text="Panel principal", fg="white", bg="#1f2937", font=("Arial", 18, "bold")).pack(side="left")
        tk.Button(header, text="Cerrar sesión", command=self.cerrar_sesion, bg="#ef4444", fg="white", padx=10, pady=4).pack(side="right")

        content = tk.Frame(self.frame, padx=18, pady=18, bg="#eef2f6")
        content.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill="both", expand=True)

        self.tab_usuarios = tk.Frame(self.notebook, bg="#ffffff")
        self.tab_productos = tk.Frame(self.notebook, bg="#ffffff")

        self.notebook.add(self.tab_usuarios, text="Usuarios")
        self.notebook.add(self.tab_productos, text="Productos")

        self._configurar_tab_usuarios()
        self._configurar_tab_productos()
        self.mostrar_usuarios()

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def _configurar_tab_usuarios(self):
        tk.Label(self.tab_usuarios, text="Consulta de usuarios", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor="w", padx=18, pady=(15, 8))
        self.tree_usuarios = ttk.Treeview(self.tab_usuarios, columns=("usuario", "rol"), show="headings", height=14)
        self.tree_usuarios.heading("usuario", text="Usuario")
        self.tree_usuarios.heading("rol", text="Rol")
        self.tree_usuarios.column("usuario", width=220, anchor="center")
        self.tree_usuarios.column("rol", width=120, anchor="center")
        self.tree_usuarios.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _configurar_tab_productos(self):
        form_frame = tk.Frame(self.tab_productos, bg="#ffffff")
        form_frame.pack(fill="x", padx=18, pady=(16, 12))

        campos = [
            ("Código", "codigo"),
            ("Nombre", "nombre"),
            ("Categoría", "categoria"),
            ("Precio", "precio"),
            ("Cantidad", "cantidad"),
        ]

        self.entradas = {}
        for index, (label_text, key) in enumerate(campos):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 10, "bold"), bg="#ffffff")
            label.grid(row=index, column=0, padx=(0, 12), pady=6, sticky="w")
            entry = tk.Entry(form_frame, width=26, font=("Arial", 10))
            entry.grid(row=index, column=1, padx=(0, 18), pady=6, sticky="w")
            self.entradas[key] = entry

        botones = tk.Frame(form_frame, bg="#ffffff")
        botones.grid(row=5, column=0, columnspan=2, sticky="w", pady=(16, 0))

        tk.Button(botones, text="Registrar", width=12, command=self.registrar_producto, bg="#2563eb", fg="white").pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Consultar", width=12, command=self.consultar_producto, bg="#0f766e", fg="white").pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Actualizar", width=12, command=self.actualizar_producto, bg="#d97706", fg="white").pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Eliminar", width=12, command=self.eliminar_producto, bg="#dc2626", fg="white").pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Limpiar", width=10, command=self.limpiar_formulario, bg="#64748b", fg="white").pack(side="left")

        self.lista_productos = ttk.Treeview(self.tab_productos, columns=("codigo", "nombre", "categoria", "precio", "cantidad"), show="headings", height=12)
        self.lista_productos.heading("codigo", text="Código")
        self.lista_productos.heading("nombre", text="Nombre")
        self.lista_productos.heading("categoria", text="Categoría")
        self.lista_productos.heading("precio", text="Precio")
        self.lista_productos.heading("cantidad", text="Stock")

        self.lista_productos.column("codigo", width=90, anchor="center")
        self.lista_productos.column("nombre", width=220)
        self.lista_productos.column("categoria", width=130, anchor="center")
        self.lista_productos.column("precio", width=110, anchor="center")
        self.lista_productos.column("cantidad", width=80, anchor="center")
        self.lista_productos.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.actualizar_tabla_productos()

    def _mostrar_mensaje(self, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror("Error", mensaje)
        else:
            messagebox.showinfo("Información", mensaje)

    def limpiar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

    def _obtener_producto_desde_formulario(self):
        codigo = self.entradas["codigo"].get().strip()
        nombre = self.entradas["nombre"].get().strip()
        categoria = self.entradas["categoria"].get().strip()
        precio = self.entradas["precio"].get().strip()
        cantidad = self.entradas["cantidad"].get().strip()

        if not codigo or not nombre:
            raise ValueError("El código y el nombre del producto son obligatorios.")

        return {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria or "general",
            "precio": float(precio) if precio else 0,
            "cantidad": int(cantidad) if cantidad else 0,
        }

    def registrar_producto(self):
        try:
            datos = self._obtener_producto_desde_formulario()
            producto = self.servicio.buscar_producto_por_codigo(datos["codigo"])
            if producto is not None:
                raise ValueError("Ya existe un producto con ese código.")
            from modelos.producto import Producto
            nuevo_producto = Producto(**datos)
            self.servicio.registrar_producto(nuevo_producto)
            self.limpiar_formulario()
            self.actualizar_tabla_productos()
            self._mostrar_mensaje("Producto registrado correctamente.")
        except Exception as exc:
            self._mostrar_mensaje(str(exc), "error")

    def consultar_producto(self):
        codigo = self.entradas["codigo"].get().strip()
        if not codigo:
            self._mostrar_mensaje("Ingrese el código del producto a consultar.", "error")
            return

        producto = self.servicio.buscar_producto_por_codigo(codigo)
        if producto is None:
            self._mostrar_mensaje("No existe un producto con ese código.", "error")
            return

        self.entradas["nombre"].delete(0, tk.END)
        self.entradas["nombre"].insert(0, producto.nombre)
        self.entradas["categoria"].delete(0, tk.END)
        self.entradas["categoria"].insert(0, producto.categoria)
        self.entradas["precio"].delete(0, tk.END)
        self.entradas["precio"].insert(0, str(producto.precio))
        self.entradas["cantidad"].delete(0, tk.END)
        self.entradas["cantidad"].insert(0, str(producto.cantidad))

    def actualizar_producto(self):
        codigo = self.entradas["codigo"].get().strip()
        if not codigo:
            self._mostrar_mensaje("Ingrese el código del producto a actualizar.", "error")
            return

        try:
            nombre = self.entradas["nombre"].get().strip() or None
            categoria = self.entradas["categoria"].get().strip() or None
            precio = self.entradas["precio"].get().strip() or None
            cantidad = self.entradas["cantidad"].get().strip() or None
            self.servicio.actualizar_producto(codigo, nombre, categoria, precio, cantidad)
            self.actualizar_tabla_productos()
            self._mostrar_mensaje("Producto actualizado correctamente.")
        except Exception as exc:
            self._mostrar_mensaje(str(exc), "error")

    def eliminar_producto(self):
        codigo = self.entradas["codigo"].get().strip()
        if not codigo:
            self._mostrar_mensaje("Ingrese el código del producto a eliminar.", "error")
            return

        try:
            eliminado = self.servicio.eliminar_producto(codigo)
            if not eliminado:
                raise ValueError("No existe un producto con ese código.")
            self.limpiar_formulario()
            self.actualizar_tabla_productos()
            self._mostrar_mensaje("Producto eliminado correctamente.")
        except Exception as exc:
            self._mostrar_mensaje(str(exc), "error")

    def actualizar_tabla_productos(self):
        for fila in self.lista_productos.get_children():
            self.lista_productos.delete(fila)

        for producto in self.servicio.listar_productos():
            self.lista_productos.insert(
                "",
                tk.END,
                values=(producto.codigo, producto.nombre, producto.categoria, f"${producto.precio:.2f}", producto.cantidad),
            )

    def mostrar_usuarios(self):
        for fila in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(fila)

        for usuario in self.servicio.listar_usuarios():
            self.tree_usuarios.insert("", tk.END, values=(usuario.nombre_usuario, usuario.rol))

    def cerrar_sesion(self):
        self.frame.pack_forget()
        self.on_logout()
