from pathlib import Path
import tkinter as tk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Restaurante App - Semana 16")
		self.root.geometry("1120x740")
		self.root.minsize(920, 620)
		base = Path(__file__).resolve().parent
		self.servicio = RestauranteServicio(
			ArchivoServicio(), base / "datos" / "productos.json",
			base / "datos" / "usuarios.json", base / "datos" / "ventas.json")
		self.login_view = LoginView(self.root, self.servicio, self.mostrar_principal)
		self.main_view = None

	def mostrar_principal(self, usuario):
		if self.main_view is None:
			self.main_view = MainView(self.root, self.servicio, self.mostrar_login, usuario)
		else:
			self.main_view.mostrar(usuario)

	def mostrar_login(self):
		self.login_view.limpiar()
		self.login_view.mostrar()

	def ejecutar(self):
		self.login_view.mostrar()
		self.root.mainloop()


if __name__ == "__main__":
	RestauranteApp().ejecutar()
