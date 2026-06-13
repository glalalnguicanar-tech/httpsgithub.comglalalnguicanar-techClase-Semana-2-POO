# ====================================================================================
# PROGRAMA DE REGISTRO DE MASCOTAS - PROGRAMACIÓN TRADICIONAL
# Utiliza funciones y variables para registrar y mostrar información de mascotas
# ====================================================================================

# Variables globales para almacenar información de mascotas
mascotas = []

# Función para solicitar datos de una mascota
def obtener_datos_mascota():
    """
    Solicita al usuario los datos de una mascota mediante teclado
    Retorna un diccionario con la información
    """
    print("\n" + "=" * 60)
    print("REGISTRO DE NUEVA MASCOTA")
    print("=" * 60)
    
    nombre = input("Ingrese el nombre de la mascota: ").strip()
    tipo = input("Ingrese el tipo de mascota (perro, gato, ave, etc.): ").strip()
    raza = input("Ingrese la raza: ").strip()
    edad = input("Ingrese la edad (en años): ").strip()
    color = input("Ingrese el color: ").strip()
    peso = input("Ingrese el peso (en kg): ").strip()
    dueno = input("Ingrese el nombre del dueño: ").strip()
    
    # Retornar diccionario con los datos
    return {
        "nombre": nombre,
        "tipo": tipo,
        "raza": raza,
        "edad": edad,
        "color": color,
        "peso": peso,
        "dueno": dueno
    }

# Función para guardar una mascota
def registrar_mascota(mascota):
    """
    Registra una mascota en la lista global
    """
    if mascota["nombre"]:  # Validar que tenga nombre
        mascotas.append(mascota)
        print("\n✓ Mascota registrada exitosamente!")
    else:
        print("\n✗ Error: La mascota debe tener un nombre.")

# Función para mostrar una mascota
def mostrar_mascota(mascota):
    """
    Muestra la información de una mascota de forma organizada
    """
    print("\n" + "-" * 60)
    print(f"Nombre:        {mascota['nombre']}")
    print(f"Tipo:          {mascota['tipo']}")
    print(f"Raza:          {mascota['raza']}")
    print(f"Edad:          {mascota['edad']} años")
    print(f"Color:         {mascota['color']}")
    print(f"Peso:          {mascota['peso']} kg")
    print(f"Dueño:         {mascota['dueno']}")
    print("-" * 60)

# Función para mostrar todas las mascotas registradas
def mostrar_todas_mascotas():
    """
    Muestra la información de todas las mascotas registradas
    """
    if len(mascotas) == 0:
        print("\n⚠ No hay mascotas registradas aún.")
    else:
        print("\n" + "=" * 60)
        print("MASCOTAS REGISTRADAS")
        print("=" * 60)
        
        for indice, mascota in enumerate(mascotas, 1):
            print(f"\nMascota #{indice}:")
            mostrar_mascota(mascota)

# Función para buscar una mascota por nombre
def buscar_mascota(nombre):
    """
    Busca una mascota por nombre en la lista
    """
    for mascota in mascotas:
        if mascota["nombre"].lower() == nombre.lower():
            return mascota
    return None

# Función para mostrar mascota por nombre
def mostrar_mascota_por_nombre():
    """
    Solicita el nombre de una mascota y la muestra si existe
    """
    nombre = input("\nIngrese el nombre de la mascota a buscar: ").strip()
    mascota = buscar_mascota(nombre)
    
    if mascota:
        print(f"\n✓ Mascota encontrada:")
        mostrar_mascota(mascota)
    else:
        print(f"\n✗ No se encontró una mascota con el nombre '{nombre}'.")

# Función para mostrar el menú principal
def mostrar_menu():
    """
    Muestra el menú de opciones disponibles
    """
    print("\n" + "=" * 60)
    print("SISTEMA DE REGISTRO DE MASCOTAS")
    print("=" * 60)
    print("1. Registrar una nueva mascota")
    print("2. Ver todas las mascotas registradas")
    print("3. Buscar una mascota por nombre")
    print("4. Salir del programa")
    print("=" * 60)

# Función principal
def main():
    """
    Función principal que controla el flujo del programa
    """
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            mascota = obtener_datos_mascota()
            registrar_mascota(mascota)
            
        elif opcion == "2":
            mostrar_todas_mascotas()
            
        elif opcion == "3":
            mostrar_mascota_por_nombre()
            
        elif opcion == "4":
            print("\n" + "=" * 60)
            print("¡Gracias por usar el sistema de registro de mascotas!")
            print("=" * 60 + "\n")
            break
            
        else:
            print("\n✗ Opción no válida. Intente de nuevo.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
