# Restaurante App - Semana 13

Aplicacion base de restaurante con una interfaz grafica sencilla construida con Tkinter. Esta version adapta la organizacion del proyecto docente: mantiene modelos, servicios y datos separados, agrega vistas en `ui/` y usa `main.py` como punto de entrada.

## Estructura

```text
restaurante_app/
├── datos/       # productos.json y usuarios.json
├── modelos/     # Producto y Usuario
├── servicios/   # ArchivoServicio y RestauranteServicio
├── ui/          # LoginView y MainView
└── main.py
```

## Flujo

Al iniciar se muestra el login. Las credenciales son validadas por `RestauranteServicio`. Despues del acceso se pueden consultar productos, usuarios y la cantidad total del inventario. Ventas se muestra como funcionalidad pendiente. Cerrar sesion regresa al login dentro de la misma ventana.

## Ejecucion

Desde la carpeta `restaurante_app` ejecute:

```bash
py -3 main.py
```

Credenciales de prueba:

- Usuario: `admin` | Contrasena: `1234`
- Usuario: `mesero` | Contrasena: `restaurante`
