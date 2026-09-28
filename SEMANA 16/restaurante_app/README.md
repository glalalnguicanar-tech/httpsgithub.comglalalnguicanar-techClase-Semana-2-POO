# Restaurante App - Semana 16

Aplicación de escritorio para un restaurante, desarrollada progresivamente desde la Semana 15 con Tkinter. Se conserva el inicio de sesión, la navegación y la gestión de productos y ventas; esta evolución amplía la sección Usuarios para demostrar el manejo de eventos y callbacks.

## Gestión de usuarios

El rol del usuario autenticado determina el acceso administrativo. Solo **Administrador** ve la pestaña Usuarios y puede gestionar cuentas de tipo **Empleado** y **Cliente**. El servicio rechaza operaciones administrativas de otros roles y protege la cuenta administradora autenticada contra su eliminación. Las contraseñas no se muestran en la tabla; al actualizar, dejar el campo vacío mantiene la contraseña existente.

El formulario permite registrar, consultar mediante selección, actualizar y eliminar usuarios. El `Treeview` muestra identificador, nombre, usuario y rol. La búsqueda del registro seleccionado se realiza por identificador mediante `RestauranteServicio`; la interfaz no accede directamente a los JSON.

## Flujo de eventos

- `<<TreeviewSelect>>` usa `bind()` para llamar al callback de selección, obtener el ID de la fila y solicitar al servicio el usuario que se carga en el formulario.
- `<<ComboboxSelected>>` usa `bind()` para responder al rol elegido y actualizar el estado visual del formulario.
- `<Return>` usa `bind()` como atajo de registro y reutiliza `registrar_usuario()`.
- `<Escape>` usa `bind()` para limpiar el formulario y cancelar la selección activa.
- Los botones Registrar, Actualizar, Eliminar y Limpiar usan `command=` para ejecutar sus callbacks.

```text
interacción -> evento/bind() o command= -> callback de interfaz
			-> RestauranteServicio -> usuarios.json -> Treeview y mensaje
```

Los callbacks recopilan valores y actualizan la vista. `RestauranteServicio` conserva validaciones, reglas de rol y operaciones; `ArchivoServicio` realiza la persistencia en `datos/usuarios.json`. Los productos y las ventas continúan guardándose en sus JSON respectivos.

## Estructura

```text
restaurante_app/
├── assets/                 # Logotipo e icono de ventas (SVG y XBM)
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
├── servicios/
├── ui/
└── main.py
```

## Ejecución

Desde esta carpeta, ejecute:

```bash
python main.py
```

La aplicación usa Tkinter, incluido en la distribución estándar de Python. Credenciales de demostración iniciales:

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `1234` |
| Empleado | `mesero` | `restaurante` |

Los usuarios agregados y sus roles se conservan en `datos/usuarios.json` al cerrar y volver a iniciar la aplicación.
