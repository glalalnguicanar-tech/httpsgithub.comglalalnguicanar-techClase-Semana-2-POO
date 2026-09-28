import tkinter as tk


class LoginView:
	def __init__(self, root, servicio, on_login):
		self.servicio = servicio
		self.on_login = on_login
		self.frame = tk.Frame(root, bg="#edf2ee", padx=40, pady=36)
		self.frame.pack(fill="both", expand=True)
		panel = tk.Frame(self.frame, bg="#fffdf8", bd=1, relief="solid", padx=30, pady=28)
		panel.pack(expand=True)
		tk.Label(panel, text="SABOR LOCAL", foreground="#176b5b", background="#fffdf8", font=("Arial", 12, "bold")).pack()
		tk.Label(panel, text="Restaurante App", foreground="#18352f", background="#fffdf8", font=("Arial", 22, "bold")).pack(pady=(4, 20))
		tk.Label(panel, text="Usuario", background="#fffdf8", font=("Arial", 10, "bold")).pack(anchor="w")
		self.usuario_entry = tk.Entry(panel, width=32, font=("Arial", 11))
		self.usuario_entry.pack(fill="x", pady=(6, 12))
		tk.Label(panel, text="Contraseña", background="#fffdf8", font=("Arial", 10, "bold")).pack(anchor="w")
		self.contrasena_entry = tk.Entry(panel, width=32, show="*", font=("Arial", 11))
		self.contrasena_entry.pack(fill="x", pady=(6, 16))
		tk.Button(panel, text="Ingresar", width=28, command=self.ingresar).pack()
		self.mensaje = tk.Label(panel, text="", fg="#b42318", bg="#fffdf8", font=("Arial", 9, "bold"))
		self.mensaje.pack(pady=(14, 0))
		self.usuario_entry.bind("<Return>", self._evento_ingresar)
		self.contrasena_entry.bind("<Return>", self._evento_ingresar)
		self.usuario_entry.focus_set()

	def _evento_ingresar(self, event):
		self.ingresar()
		return "break"

	def ingresar(self):
		nombre_usuario = self.usuario_entry.get().strip()
		contrasena = self.contrasena_entry.get()
		if not nombre_usuario or not contrasena:
			self.mensaje.config(text="Ingrese usuario y contraseña.")
			return
		usuario = self.servicio.autenticar(nombre_usuario, contrasena)
		if usuario is None:
			self.mensaje.config(text="Las credenciales no son válidas.")
			return
		self.frame.pack_forget()
		self.on_login(usuario)

	def mostrar(self):
		self.frame.pack(fill="both", expand=True)
		self.usuario_entry.focus_set()

	def limpiar(self):
		self.usuario_entry.delete(0, tk.END)
		self.contrasena_entry.delete(0, tk.END)
		self.mensaje.config(text="")
