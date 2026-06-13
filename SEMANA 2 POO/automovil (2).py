# Clase Automóvil - Ejercicio de POO Semana 2
# Clase relacionada con un objeto del mundo real

class Automovil:
    """Clase que representa un automóvil con sus atributos y métodos"""
    
    def __init__(self, marca, modelo, año, velocidad_maxima):
        # Atributos de la clase
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.velocidad_maxima = velocidad_maxima
        self.velocidad_actual = 0  # Atributo adicional
        self.encendido = False
    
    def encender(self):
        """Método para encender el automóvil"""
        if not self.encendido:
            self.encendido = True
            print(f"✓ El {self.marca} {self.modelo} ha sido encendido")
        else:
            print(f"El {self.marca} {self.modelo} ya estaba encendido")
    
    def acelerar(self, incremento):
        """Método para acelerar el automóvil"""
        if not self.encendido:
            print(f"Error: Debes encender el {self.marca} {self.modelo} primero")
            return
        
        self.velocidad_actual += incremento
        
        if self.velocidad_actual > self.velocidad_maxima:
            self.velocidad_actual = self.velocidad_maxima
            print(f"⚠ {self.marca} {self.modelo} alcanzó su velocidad máxima: {self.velocidad_actual} km/h")
        else:
            print(f"⚡ {self.marca} {self.modelo} aceleró a {self.velocidad_actual} km/h")
    
    def frenar(self, decremento):
        """Método para frenar el automóvil"""
        if not self.encendido:
            print(f"Error: El {self.marca} {self.modelo} no está encendido")
            return
        
        self.velocidad_actual -= decremento
        
        if self.velocidad_actual < 0:
            self.velocidad_actual = 0
            print(f"🛑 {self.marca} {self.modelo} se detuvo completamente")
        else:
            print(f"🛑 {self.marca} {self.modelo} frenó a {self.velocidad_actual} km/h")
    
    def obtener_informacion(self):
        """Método para obtener la información del automóvil"""
        estado = "Encendido" if self.encendido else "Apagado"
        print(f"\n--- Información del Automóvil ---")
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Año: {self.año}")
        print(f"Velocidad Máxima: {self.velocidad_maxima} km/h")
        print(f"Velocidad Actual: {self.velocidad_actual} km/h")
        print(f"Estado: {estado}")
        print("-" * 35)


# Crear dos objetos diferentes de la clase Automovil
if __name__ == "__main__":
    print("=" * 40)
    print("EJERCICIO DE POO - CLASE AUTOMÓVIL")
    print("=" * 40)
    
    # Objeto 1: Auto deportivo
    print("\n📍 Creando primer automóvil...")
    auto1 = Automovil("Ferrari", "F8 Tributo", 2023, 340)
    auto1.obtener_informacion()
    
    print("\n🚗 Simulando conducción del Ferrari:")
    auto1.encender()
    auto1.acelerar(80)
    auto1.acelerar(120)
    auto1.acelerar(100)
    auto1.frenar(50)
    auto1.frenar(100)
    auto1.obtener_informacion()
    
    # Objeto 2: Auto familiar
    print("\n" + "=" * 40)
    print("\n📍 Creando segundo automóvil...")
    auto2 = Automovil("Toyota", "Corolla", 2022, 180)
    auto2.obtener_informacion()
    
    print("\n🚗 Simulando conducción del Toyota:")
    auto2.encender()
    auto2.acelerar(50)
    auto2.acelerar(60)
    auto2.acelerar(70)
    auto2.frenar(80)
    auto2.obtener_informacion()
    
    print("\n" + "=" * 40)
    print("✅ Programa completado exitosamente")
    print("=" * 40)