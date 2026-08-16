# Restaurante App - Semana 9

Este proyecto implementa un sistema modular para administrar productos y usuarios de un restaurante.

## Estructura del proyecto

- modelos/producto.py: define la clase Producto con código, nombre, categoría y precio.
- modelos/usuario.py: define la clase Usuario con identificación, nombre y correo.
- servicios/restaurante.py: administra las colecciones, búsquedas, registros, actualizaciones y eliminaciones.
- main.py: presenta un menú interactivo para usar las funcionalidades del sistema.

## Estructuras de datos utilizadas

- Lista: almacena los productos y usuarios registrados.
- Tupla: representa las opciones fijas del menú principal.
- Diccionario: asocia las opciones del menú con las acciones correspondientes.
- Conjunto: muestra las categorías únicas de los productos registrados.

## Funcionalidades

- Registrar productos.
- Buscar productos por código.
- Actualizar productos.
- Eliminar productos.
- Listar productos.
- Registrar usuarios.
- Listar usuarios.
- Mostrar categorías únicas.

## Ejecución

Ejecute el programa desde la carpeta del proyecto con:

```bash
python main.py
```
