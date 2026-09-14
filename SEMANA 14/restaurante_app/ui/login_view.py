import tkinter as tk
from tkinter import messagebox


class LoginView:
    def __init__(self, root, servicio, on_login):
        self.root = root
        self.servicio = servicio
        self.on_login = on_login

        self.frame = tk.Frame(root, padx=40, pady=36, bg="#f4f4f4")
        self.frame.pack(fill="both", expand=True)

        panel = tk.Frame(self.frame, bg="#ffffff", bd=1, relief="solid", padx=26, pady=26)
        panel.pack(expand=True)

        tk.Label(panel, text="Restaurante App", font=("Arial", 22, "bold"), bg="#ffffff").pack(pady=(0, 20))
        tk.Label(panel, text="Usuario", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w")
        self.usuario_entry = tk.Entry(panel, width=32, font=("Arial", 11))
        self.usuario_entry.pack(fill="x", pady=(6, 12))

        tk.Label(panel, text="Contraseña", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w")
        self.contrasena_entry = tk.Entry(panel, width=32, show="*", font=("Arial", 11))
        self.contrasena_entry.pack(fill="x", pady=(6, 16))

        self.boton_login = tk.Button(panel, text="Ingresar", width=28, command=self.ingresar, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"))
        self.boton_login.pack()

        self.mensaje = tk.Label(panel, text="", fg="#b71c1c", bg="#ffffff", font=("Arial", 9, "bold"))
        self.mensaje.pack(pady=(14, 0))

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
        self.frame.pack(fill="both", expand=True)
        self.usuario_entry.focus_set()

    def limpiar(self):
        self.usuario_entry.delete(0, tk.END)
        self.contrasena_entry.delete(0, tk.END)
        self.mensaje.config(text="")
