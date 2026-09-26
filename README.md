# Sistema de Gestión de Restaurante - Semana 15

Aplicación de Escritorio desarrollada en Python utilizando **Tkinter**, diseñada bajo una arquitectura modular y orientada a objetos para la gestión integral de un restaurante (usuarios, productos y ventas), cumpliendo estrictamente con los estándares visuales y funcionales de diseño.

Propósito de la Semana 15

El objetivo principal de esta práctica es consolidar el desarrollo de interfaces gráficas de usuario (GUI) profesionales mediante el uso de **Tkinter** y **ttk**, integrando estilos visuales coherentes (tema *clam*), manejo dinámico y multiplataforma de recursos multimedia (iconos y logotipos con Pillow), y la implementación de un módulo transaccional completo con persistencia local en JSON.

Evolución sobre el Proyecto Anterior

* **Refinamiento Visual:** Transición hacia una paleta de colores corporativa basada en tonos azules y celestes, alineada con las especificaciones del diseño de referencia.
* **Optimización de Assets:** Implementación de carga segura de imágenes y escalado automático de iconos (18x18px) en botones mediante el uso de Pillow (`PIL`), eliminando problemas de compatibilidad y tamaños desproporcionados.
* **Navegación Fluida y Sesiones:** Integración de un panel lateral de control interactivo con control de roles y un flujo seguro de cierre de sesión que redirige limpiamente al módulo de autenticación.

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

Nueva Gestión de Ventas

El sistema incorpora un módulo robusto para el registro y control de ventas:
* Selección dinámica de usuarios registrados y productos disponibles mediante menús desplegables (`ttk.Combobox`).
* Cálculo automático del costo total de la transacción basado en el precio del producto seleccionado.
* Actualización en tiempo real de las tablas de visualización y de los contadores métricos en la barra de estado.

Uso de `command=` y Callbacks

La aplicación implementa un patrón basado en eventos y referencias a funciones:
* Los botones interactivos de la barra lateral y del panel de gestión utilizan el parámetro `command=` enlazado a **callbacks** específicos (ej. `_callback_registrar_venta`, `mostrar_seccion`, `_cerrar_sesion`).
* Esto permite modularizar las acciones del usuario, manteniendo el código limpio, desacoplado y de fácil mantenimiento.

Persistencia en `ventas.json`
* Toda la información transaccional generada en el sistema se almacena de forma persistente en archivos locales con formato JSON (como `ventas.json`).
* Garantiza que el historial de ventas, el registro de productos y los usuarios no se pierdan al cerrar la aplicación, recargándose automáticamente en cada ejecución.

Pasos para Ejecutar el Proyecto

Abrir la terminal o tu entorno de desarrollo (como VS Code) posicionándote en la carpeta raíz del proyecto.

Ejecutar el archivo principal con el siguiente comando:

Bash
python main.py
¡Listo! Utiliza las credenciales de administrador correspondientes para iniciar sesión y explorar el sistema.  