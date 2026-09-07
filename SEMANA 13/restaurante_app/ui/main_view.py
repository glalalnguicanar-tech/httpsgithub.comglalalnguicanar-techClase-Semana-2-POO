import tkinter as tk


class MainView:
	def __init__(self, root, servicio, on_logout):
		self.root = root
		self.servicio = servicio
		self.on_logout = on_logout
		self.frame = tk.Frame(root, padx=24, pady=24)
		self.frame.pack(fill="both", expand=True)

		encabezado = tk.Frame(self.frame)
		encabezado.pack(fill="x")
		tk.Label(encabezado, text="Panel principal", font=("Arial", 18, "bold")).pack(side="left")
		tk.Button(encabezado, text="Cerrar sesión", command=self.cerrar_sesion).pack(side="right")
		tk.Label(self.frame, text="Seleccione una opción para consultar la información registrada.").pack(anchor="w", pady=(8, 16))

		botones = tk.Frame(self.frame)
		botones.pack(fill="x")
		tk.Button(botones, text="Productos", command=self.mostrar_productos).pack(side="left", padx=(0, 8))
		tk.Button(botones, text="Usuarios", command=self.mostrar_usuarios).pack(side="left", padx=(0, 8))
		tk.Button(botones, text="Ventas (pendiente)", command=self.mostrar_pendiente).pack(side="left")

		self.contenido = tk.Text(self.frame, height=14, width=70, state="disabled")
		self.contenido.pack(fill="both", expand=True, pady=(16, 0))
		self.mostrar_productos()

	def _escribir(self, texto):
		self.contenido.config(state="normal")
		self.contenido.delete("1.0", tk.END)
		self.contenido.insert(tk.END, texto)
		self.contenido.config(state="disabled")

	def mostrar_productos(self):
		productos = self.servicio.listar_productos()
		lineas = ["PRODUCTOS REGISTRADOS", "=" * 24]
		lineas.extend(str(producto) for producto in productos)
		lineas.append(f"\nCantidad total en inventario: {self.servicio.consultar_cantidad_productos()}")
		self._escribir("\n".join(lineas))

	def mostrar_usuarios(self):
		usuarios = self.servicio.listar_usuarios()
		lineas = ["USUARIOS REGISTRADOS", "=" * 22]
		lineas.extend(str(usuario) for usuario in usuarios)
		self._escribir("\n".join(lineas))

	def mostrar_pendiente(self):
		self._escribir("La gestión de ventas estará disponible en una etapa posterior.")

	def cerrar_sesion(self):
		self.frame.pack_forget()
		self.on_logout()
