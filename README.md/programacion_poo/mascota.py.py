class Mascota:

    def __init__(self, nombre, especie, edad):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

    def mostrar_informacion(self):
        print("\n--- INFORMACIÓN DE LA MASCOTA ---")
        print("Nombre:", self.nombre)
        print("Especie:", self.especie)
        print("Edad:", self.edad)

    def hacer_sonido(self):
        print(self.nombre, "hace un sonido.")