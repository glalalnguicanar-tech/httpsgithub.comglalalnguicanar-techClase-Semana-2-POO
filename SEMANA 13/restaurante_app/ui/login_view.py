import tkinter as tk
from tkinter import messagebox


class LoginView:
	def __init__(self, root, servicio, on_login):
		self.root = root
		self.servicio = servicio
		self.on_login = on_login
		self.frame = tk.Frame(root, padx=32, pady=28)
		self.frame.pack(expand=True)

		tk.Label(self.frame, text="Restaurante App", font=("Arial", 20, "bold")).pack(pady=(0, 18))
		tk.Label(self.frame, text="Usuario").pack(anchor="w")
		self.usuario_entry = tk.Entry(self.frame, width=30)
		self.usuario_entry.pack(pady=(0, 10))
		tk.Label(self.frame, text="Contraseña").pack(anchor="w")
		self.contrasena_entry = tk.Entry(self.frame, width=30, show="*")
		self.contrasena_entry.pack(pady=(0, 16))
		tk.Button(self.frame, text="Ingresar", width=24, command=self.ingresar).pack()
		self.mensaje = tk.Label(self.frame, text="", fg="firebrick")
		self.mensaje.pack(pady=(12, 0))
		self.usuario_entry.focus_set()

	def ingresar(self):
		nombre_usuario = self.usuario_entry.get().strip()
		contrasena = self.contrasena_entry.get()
		if not nombre_usuario or not contrasena:
			self.mensaje.config(text="Ingrese usuario y contraseña.")
			return
		if not self.servicio.validar_acceso(nombre_usuario, contrasena):
			self.mensaje.config(text="Las credenciales no son válidas.")
			return
		self.frame.pack_forget()
		self.on_login()

	def mostrar(self):
		self.frame.pack(expand=True)
		self.usuario_entry.focus_set()

	def limpiar(self):
		self.usuario_entry.delete(0, tk.END)
		self.contrasena_entry.delete(0, tk.END)
		self.mensaje.config(text="")
