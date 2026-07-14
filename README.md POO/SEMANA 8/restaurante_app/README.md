# Restaurante App

Este proyecto implementa un sistema modular de registro y listado para un restaurante.

## Archivos principales

- `modelos/producto.py`: define la clase `Producto` y su método `mostrar_informacion()`.
- `modelos/bebida.py`: define la clase `Bebida`, que hereda de `Producto` y agrega atributos específicos.
- `modelos/cliente.py`: define la clase `Cliente` y su método `mostrar_informacion()`.
- `servicios/restaurante.py`: define la clase `Restaurante`, que administra productos y clientes.
- `main.py`: punto de entrada que muestra un menú interactivo y solicita datos por consola.

## Uso

Ejecutar el programa desde la carpeta `restaurante_app`:

```bash
python main.py
```

El menú permite registrar productos, bebidas y clientes, y listar los registros guardados.
