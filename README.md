Restaurante App - Semana 16 

Propósito de la Semana 16

El objetivo de esta actividad es aplicar de manera práctica el **manejo de eventos en Tkinter** dentro del proyecto evolucionado `restaurante_app`. La gestión de usuarios se utiliza como contexto principal para demostrar cómo las interacciones del usuario (clics, selecciones en tablas y atajos de teclado) activan respuestas dinámicas en la interfaz sin saturar la lógica del sistema.

Estructura del sistema 

├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   ├── assets/              
│   └── main.py
└── README.md


Evolución del Proyecto

Este proyecto da continuidad al desarrollo de las semanas anteriores, conservando la arquitectura modular limpia y separando responsabilidades entre:
- Datos (`datos/`): Archivos JSON locales (`usuarios.json`, `productos.json`, `ventas.json`).
- Modelos (`modelos/`): Clases orientadas a objetos (`Usuario`, `Producto`, `Venta`).
- Servicios (`servicios/`): Capa de lógica de negocio y persistencia (`RestauranteServicio`, `ArchivoServicio`).
- Interfaz (`ui/`): Vistas de autenticación (`LoginView`) y panel principal (`MainView`).
- Recursos (`assets/`): Íconos interactivos y logotipos del sistema.

En esta semana se amplió específicamente la sección de **Gestión de Usuarios**, incorporando el control de roles y el manejo avanzado de eventos y atajos de teclado.


Gestión de Usuarios y Roles

- Roles incorporados: Se añadió el atributo `rol` a la entidad `Usuario`, permitiendo diferenciar tres perfiles en el sistema:

  1. Administrador: Cuenta con privilegios completos para acceder al módulo de gestión de usuarios (CRUD completo) y supervisar el restaurante.
  2. Mesero / Empleado: Perfil operativo con acceso limitado.
  3. Cliente: Perfil consumidor.
- Control de Acceso: La aplicación restringe la vista y el acceso a la sección de administración de usuarios exclusivamente a los usuarios con rol de Administrador.

Manejo de Eventos, `bind()`, `command=` y Callbacks

La aplicación implementa claramente la distinción entre los mecanismos de interacción:
- `command=`: Utilizado en los botones principales de la interfaz (`Registrar`, `Actualizar`, `Eliminar`, `Limpiar`) para disparar las acciones directas del CRUD.
- `bind()`: Utilizado para asociar eventos avanzados e interactivos:
- `<<TreeviewSelect>>`: Vinculado a la tabla de usuarios para que, al seleccionar cualquier fila, los datos del registro se carguen de forma automática y dinámica en el formulario de edición.
- `<<ComboboxSelected>>`: Vinculado al selector de roles para responder en tiempo real a los cambios de perfil y reflejar el estado en la barra inferior.


  - Atajos de teclado (`<Return>` y `<Escape>`): 
    - `<Return>` (Enter): Permite confirmar y ejecutar el registro de un usuario directamente desde el formulario mediante el teclado.
    - `<Escape>` (Esc): Limpia los campos del formulario y desmarca la selección actual en la tabla.
- **Callbacks:** Funciones intermedias que capturan los eventos de la interfaz y delegan la ejecución a `RestauranteServicio`, evitando duplicar código y manteniendo separada la lógica de negocio de la interfaz gráfica.

Persistencia de Datos

La persistencia de la información se gestiona de manera transparente mediante archivos en formato JSON (`usuarios.json`). 
- Las operaciones de registro, actualización y eliminación modifican los objetos en memoria y son guardadas automáticamente en el archivo local a través de `RestauranteServicio` y `ArchivoServicio`, garantizando que los datos se recuperen correctamente al reiniciar la aplicación.
- **Medida de seguridad:** Se incluyó una validación preventiva para evitar que el usuario Administrador actualmente autenticado pueda eliminarse a sí mismo por error desde la interfaz.

Pasos para Ejecutar la Aplicación (`main.py`)

1. Tener instalado **Python** y las librerías necesarias (como `Pillow` para la gestión de imágenes en `assets/`).
2. Abre una terminal en la raíz del proyecto.
3. Ejecuta el archivo principal con el siguiente comando:
   python main.py