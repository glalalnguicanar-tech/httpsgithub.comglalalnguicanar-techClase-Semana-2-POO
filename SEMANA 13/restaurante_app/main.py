from pathlib import Path
import tkinter as tk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Restaurante App")
		self.root.geometry("640x430")
		self.root.minsize(560, 360)

		base = Path(__file__).resolve().parent
		archivo_servicio = ArchivoServicio()
		self.servicio = RestauranteServicio(
			archivo_servicio,
			base / "datos" / "productos.json",
			base / "datos" / "usuarios.json",
		)
		self.login_view = LoginView(self.root, self.servicio, self.mostrar_principal)
		self.main_view = None

	def mostrar_principal(self):
		self.main_view = MainView(self.root, self.servicio, self.mostrar_login)

	def mostrar_login(self):
		self.login_view.limpiar()
		self.login_view.mostrar()

	def ejecutar(self):
		self.root.mainloop()


if __name__ == "__main__":
	RestauranteApp().ejecutar()
