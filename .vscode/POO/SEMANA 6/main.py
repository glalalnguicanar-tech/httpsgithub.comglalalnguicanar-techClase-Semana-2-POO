from modelos.bebida import Bebida
from modelos.platillo import Platillo
from servicios.restaurante import Restaurante


def main():
    restaurante = Restaurante()

    plato_principal = Platillo("Paella", 18000, 650, 40, True)
    bebida = Bebida("Limonada", 5000, 350, "Natural", True)

    restaurante.agregar_producto(plato_principal)
    restaurante.agregar_producto(bebida)

    print("Menú del restaurante")
    print("-------------------")
    restaurante.mostrar_productos()
    print("-------------------")
    print(f"Productos disponibles: {len(restaurante.productos_disponibles())}")


if __name__ == "__main__":
    main()
