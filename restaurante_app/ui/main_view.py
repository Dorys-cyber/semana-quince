import os
import tkinter as tk
from tkinter import ttk, messagebox

# Intentar importar PIL para redimensionar los iconos automáticamente
try:
    from PIL import Image, ImageTk
    EXIS_PIL = True
except ImportError:
    EXIS_PIL = False

class MainView(tk.Tk):
    def __init__(self, servicio, usuario_actual, on_logout=None):
        super().__init__()
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.title("Restaurante - Tkinter")
        self.geometry("950x600")
        self.configure(bg="#f8fafc")

        # Cargar los iconos antes de crear la interfaz
        self._cargar_iconos_sidebar()

        self._configurar_estilos()
        self._crear_interfaz()
        self.mostrar_seccion("inicio")

    def _cargar_iconos_sidebar(self):
        """Carga y redimensiona los iconos para la barra lateral y botones desde assets/icons."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        raiz_proyecto = os.path.dirname(base_dir)
        ruta_icons = os.path.join(raiz_proyecto, 'assets', 'icons') 

        def cargar(nombre):
            ruta = os.path.join(ruta_icons, nombre)
            if os.path.exists(ruta):
                try:
                    if EXIS_PIL:
                        img = Image.open(ruta)
                        img = img.resize((18, 18), Image.Resampling.LANCZOS)
                        return ImageTk.PhotoImage(img)
                    else:
                        return tk.PhotoImage(file=ruta)
                except Exception as e:
                    print(f"Error cargando icono {nombre}: {e}")
            else:
                print(f"No se encontró el archivo: {ruta}")
            return None

        # Iconos del menú lateral
        self.icon_home = cargar("home.png")
        self.icon_users = cargar("users.png")
        self.icon_products = cargar("products.png")
        self.icon_sales = cargar("sales.png")
        self.icon_logout = cargar("logout.png")

        # Iconos para los botones de acción
        self.icon_add = cargar("add.png")        # Registrar (+)
        self.icon_search = cargar("search.png")   # Cargar por código (lupa)
        self.icon_edit = cargar("edit.png")      # Actualizar (lápiz)
        self.icon_delete = cargar("delete.png")  # Eliminar (basurero)
        self.icon_clear = cargar("clean.png")    # Limpiar (escoba)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#dbeafe", foreground="#1e293b", font=("Arial", 9, "bold"))
        style.map("Treeview.Heading", background=[('active', '#bfdbfe')])

    def _crear_interfaz(self):
        # 1. Barra de estado inferior
        self.status_bar = tk.Label(
            self, text="", font=("Arial", 9),
            fg="#1e40af", bg="#dbeafe", anchor="w", padx=20, pady=8
        )
        self.status_bar.pack(side="bottom", fill="x")

        # 2. Menú Lateral Izquierdo
        self.sidebar = tk.Frame(self, bg="#1e293b", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Encabezado lateral
        tk.Label(self.sidebar, text="RESTAURANTE", font=("Arial", 16, "bold"), fg="white", bg="#1e293b").pack(anchor="w", padx=20, pady=(20, 2))
        tk.Label(self.sidebar, text=f"Sesión: {self.usuario_actual.rol}", font=("Arial", 10), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=20, pady=(0, 20))

        # Botones de navegación
        self.btn_inicio = self._crear_boton_sidebar(" Inicio", self.icon_home, lambda: self.mostrar_seccion("inicio"))
        self.btn_usuarios = self._crear_boton_sidebar(" Usuarios", self.icon_users, lambda: self.mostrar_seccion("usuarios"))
        self.btn_productos = self._crear_boton_sidebar(" Productos", self.icon_products, lambda: self.mostrar_seccion("productos"))
        self.btn_ventas = self._crear_boton_sidebar(" Ventas", self.icon_sales, lambda: self.mostrar_seccion("ventas"))

        # Botón Cerrar sesión
        btn_logout = tk.Button(
            self.sidebar, text=" Cerrar sesión", image=self.icon_logout, compound="left",
            font=("Arial", 10, "bold"), fg="white", bg="#f43f5e", activebackground="#e11d48", 
            activeforeground="white", bd=0, anchor="w", padx=15, cursor="hand2", command=self._callback_logout
        )
        btn_logout.pack(side="bottom", fill="x", ipady=8, padx=15, pady=20)

        # 3. Área de Contenido Principal
        self.content_area = tk.Frame(self, bg="#f8fafc")
        self.content_area.pack(side="right", expand=True, fill="both")

    def _callback_logout(self):
        self.destroy()
        if self.on_logout:
            self.on_logout()

    def _crear_boton_sidebar(self, texto, icono, comando):
        btn = tk.Button(
            self.sidebar, text=texto, image=icono, compound="left",
            font=("Arial", 11), fg="#e2e8f0", bg="#1e293b", 
            activebackground="#2563eb", activeforeground="white",
            bd=0, anchor="w", padx=15, cursor="hand2", command=comando
        )
        btn.pack(fill="x", ipady=8, pady=2)
        return btn

    def mostrar_seccion(self, seccion):
        for widget in self.content_area.winfo_children():
            widget.destroy()

        for btn in [self.btn_inicio, self.btn_usuarios, self.btn_productos, self.btn_ventas]:
            btn.configure(bg="#1e293b", fg="#e2e8f0")

        u_cnt = len(self.servicio.obtener_usuarios())
        p_cnt = len(self.servicio.obtener_productos())
        v_cnt = len(self.servicio.obtener_ventas())

        self.status_bar.config(text=f"Productos: {p_cnt} | Usuarios: {u_cnt} | Ventas: {v_cnt} | Datos JSON locales")

        if seccion == "inicio":
            self.btn_inicio.configure(bg="#2563eb", fg="white")
            self._render_inicio(u_cnt, p_cnt, v_cnt)
        elif seccion == "usuarios":
            # REQUISITO SEMANA 16: Control de acceso exclusivo para Administrador
            if self.usuario_actual.rol != "Administrador":
                messagebox.showerror("Acceso denegado", "Solo el Administrador puede acceder a la gestión de usuarios.")
                self.mostrar_seccion("inicio")
                return
            self.btn_usuarios.configure(bg="#2563eb", fg="white")
            self._render_usuarios()
        elif seccion == "productos":
            self.btn_productos.configure(bg="#2563eb", fg="white")
            self._render_productos()
        elif seccion == "ventas":
            self.btn_ventas.configure(bg="#2563eb", fg="white")
            self._render_ventas()

    def _render_inicio(self, u_count, p_count, v_count):
        header = tk.Frame(self.content_area, bg="#f8fafc")
        header.pack(fill="x", padx=30, pady=(25, 10))

        tk.Label(header, text="Panel principal", font=("Arial", 20, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w")
        tk.Label(header, text="Restaurante - Inicio de sesión exitoso. Consulte usuarios, gestione productos y registre ventas.", font=("Arial", 11), fg="#64748b", bg="#f8fafc").pack(anchor="w", pady=(2, 0))

        cards_frame = tk.Frame(self.content_area, bg="#f8fafc")
        cards_frame.pack(fill="x", padx=30, pady=20)

        self._crear_tarjeta_metrica(cards_frame, "Usuarios registrados", str(u_count), 0)
        self._crear_tarjeta_metrica(cards_frame, "Productos registrados", str(p_count), 1)
        self._crear_tarjeta_metrica(cards_frame, "Ventas registradas", str(v_count), 2)

    def _crear_tarjeta_metrica(self, parent, titulo, valor, col):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid")
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        tk.Label(card, text=titulo, font=("Arial", 10, "bold"), fg="#334155", bg="white").pack(anchor="w", padx=20, pady=(15, 5))
        tk.Label(card, text=valor, font=("Arial", 28, "bold"), fg="#2563eb", bg="white").pack(anchor="w", padx=20, pady=(0, 15))

    # ==================== SECCIÓN USUARIOS ====================
    def _render_usuarios(self):
        tk.Label(self.content_area, text="Gestión de usuarios", font=("Arial", 18, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w", padx=30, pady=(15, 5))

        main_container = tk.Frame(self.content_area, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=30, pady=10)

        left_frame = tk.Frame(main_container, bg="#f8fafc")
        left_frame.pack(side="left", fill="y", padx=(0, 15))

        form_frame = tk.LabelFrame(left_frame, text=" Datos del usuario ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 15))

        tk.Label(form_frame, text="Identificador", font=("Arial", 9), bg="white", fg="#475569").grid(row=0, column=0, sticky="w", pady=4)
        self.txt_user_id = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_user_id.grid(row=0, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Nombre", font=("Arial", 9), bg="white", fg="#475569").grid(row=1, column=0, sticky="w", pady=4)
        self.txt_user_nombre = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_user_nombre.grid(row=1, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Usuario", font=("Arial", 9), bg="white", fg="#475569").grid(row=2, column=0, sticky="w", pady=4)
        self.txt_user_username = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_user_username.grid(row=2, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Contrasena", font=("Arial", 9), bg="white", fg="#475569").grid(row=3, column=0, sticky="w", pady=4)
        self.txt_user_password = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22, show="*")
        self.txt_user_password.grid(row=3, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Rol", font=("Arial", 9), bg="white", fg="#475569").grid(row=4, column=0, sticky="w", pady=4)
        self.cbo_user_rol = ttk.Combobox(form_frame, values=["Administrador", "Mesero", "Cliente"], state="readonly", width=20)
        self.cbo_user_rol.grid(row=4, column=1, pady=4, padx=(10, 0))
        self.cbo_user_rol.set("Cliente")

        # Botones de usuarios conectados a sus acciones
        tk.Button(left_frame, text=" Registrar", image=self.icon_add, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", activebackground="#1d4ed8", bd=0, cursor="hand2", anchor="w", padx=12, command=self._registrar_usuario_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Actualizar", image=self.icon_edit, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", activebackground="#1d4ed8", bd=0, cursor="hand2", anchor="w", padx=12, command=self._actualizar_usuario_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Eliminar", image=self.icon_delete, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#f43f5e", activebackground="#e11d48", bd=0, cursor="hand2", anchor="w", padx=12, command=self._eliminar_usuario_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Limpiar", image=self.icon_clear, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#1e293b", activebackground="#334155", bd=0, cursor="hand2", anchor="w", padx=12, command=self._limpiar_usuario_accion).pack(fill="x", ipady=5, pady=3)

        right_frame = tk.LabelFrame(main_container, text=" Usuarios registrados ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        container_tree = tk.Frame(right_frame, bg="white")
        container_tree.pack(fill="both", expand=True)

        self.tree_usuarios = ttk.Treeview(container_tree, columns=("ID", "Nombre", "Username", "Rol"), show="headings")
        self.tree_usuarios.heading("ID", text="Identificador")
        self.tree_usuarios.heading("Nombre", text="Nombre")
        self.tree_usuarios.heading("Username", text="Usuario")
        self.tree_usuarios.heading("Rol", text="Rol")

        self.tree_usuarios.column("ID", width=100, anchor="center")
        self.tree_usuarios.column("Nombre", width=140, anchor="w")
        self.tree_usuarios.column("Username", width=110, anchor="w")
        self.tree_usuarios.column("Rol", width=100, anchor="w")

        scrollbar = ttk.Scrollbar(container_tree, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ==========================================================
        # REQUISITOS DE EVENTOS - SEMANA 16 (Añadidos correctamente)
        # ==========================================================
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._cargar_usuario_seleccionado)
        self.cbo_user_rol.bind("<<ComboboxSelected>>", self._callback_combobox_rol)
        
        # Atajos de teclado <Return> en los campos del formulario
        self.txt_user_id.bind("<Return>", self._callback_tecla_return)
        self.txt_user_nombre.bind("<Return>", self._callback_tecla_return)
        self.txt_user_username.bind("<Return>", self._callback_tecla_return)
        self.txt_user_password.bind("<Return>", self._callback_tecla_return)
        
        # Atajo global <Escape> para limpiar formulario y selecciones
        self.bind("<Escape>", self._callback_tecla_escape)

        self._cargar_tabla_usuarios()

    def _cargar_tabla_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        for u in self.servicio.obtener_usuarios():
            self.tree_usuarios.insert("", "end", values=(u.id, u.nombre, u.username, u.rol))

    def _limpiar_usuario_accion(self):
        self.txt_user_id.delete(0, tk.END)
        self.txt_user_nombre.delete(0, tk.END)
        self.txt_user_username.delete(0, tk.END)
        self.txt_user_password.delete(0, tk.END)
        self.cbo_user_rol.set("Cliente")

    def _cargar_usuario_seleccionado(self, event):
        seleccion = self.tree_usuarios.selection()
        if seleccion:
            item = self.tree_usuarios.item(seleccion)
            valores = item['values']
            if valores:
                self.txt_user_id.delete(0, tk.END)
                self.txt_user_id.insert(0, valores[0])
                self.txt_user_nombre.delete(0, tk.END)
                self.txt_user_nombre.insert(0, valores[1])
                self.txt_user_username.delete(0, tk.END)
                self.txt_user_username.insert(0, valores[2])
                self.cbo_user_rol.set(valores[3])

    # ==========================================================
    # NUEVOS CALLBACKS DE EVENTOS - SEMANA 16
    # ==========================================================
    def _callback_combobox_rol(self, event):
        rol_seleccionado = self.cbo_user_rol.get()
        self.status_bar.config(text=f"Rol seleccionado (<<ComboboxSelected>>): {rol_seleccionado}")

    def _callback_tecla_return(self, event):
        self._registrar_usuario_accion()

    def _callback_tecla_escape(self, event):
        self._limpiar_usuario_accion()
        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())
        self.status_bar.config(text="Formulario limpiado y selección cancelada con <Escape>.")

    def _registrar_usuario_accion(self):
        uid = self.txt_user_id.get().strip()
        nombre = self.txt_user_nombre.get().strip()
        username = self.txt_user_username.get().strip()
        password = self.txt_user_password.get().strip()
        rol = self.cbo_user_rol.get()

        if not uid or not nombre or not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos del usuario.")
            return

        exito, mensaje = self.servicio.registrar_usuario(uid, nombre, username, password, rol)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._cargar_tabla_usuarios()
            self._limpiar_usuario_accion()
        else:
            messagebox.showerror("Error", mensaje)

    def _actualizar_usuario_accion(self):
        uid = self.txt_user_id.get().strip()
        nombre = self.txt_user_nombre.get().strip()
        username = self.txt_user_username.get().strip()
        password = self.txt_user_password.get().strip()
        rol = self.cbo_user_rol.get()

        if not uid:
            messagebox.showwarning("Atención", "Ingrese o seleccione el identificador del usuario a actualizar.")
            return

        exito, mensaje = self.servicio.actualizar_usuario(uid, nombre, username, password, rol)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._cargar_tabla_usuarios()
            self._limpiar_usuario_accion()
        else:
            messagebox.showerror("Error", mensaje)

    def _eliminar_usuario_accion(self):
        uid = self.txt_user_id.get().strip()
        if not uid:
            messagebox.showwarning("Atención", "Seleccione o ingrese el ID del usuario a eliminar.")
            return

        # REQUISITO DE SEGURIDAD: Evitar eliminar la cuenta de administrador activa actual
        if self.usuario_actual.id == uid or self.usuario_actual.username == uid:
            messagebox.showerror("Seguridad", "No se puede eliminar la cuenta de administrador actualmente en sesión.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario {uid}?"):
            exito, mensaje = self.servicio.eliminar_usuario(uid)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_tabla_usuarios()
                self._limpiar_usuario_accion()
            else:
                messagebox.showerror("Error", mensaje)

    # ==================== SECCIÓN PRODUCTOS ====================
    def _render_productos(self):
        tk.Label(self.content_area, text="Gestión de Productos", font=("Arial", 18, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w", padx=30, pady=(15, 5))

        main_container = tk.Frame(self.content_area, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=30, pady=10)

        left_frame = tk.Frame(main_container, bg="#f8fafc")
        left_frame.pack(side="left", fill="y", padx=(0, 15))

        form_frame = tk.LabelFrame(left_frame, text=" Datos del producto ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 15))

        tk.Label(form_frame, text="Código", font=("Arial", 9), bg="white", fg="#475569").grid(row=0, column=0, sticky="w", pady=4)
        self.txt_prod_id = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_prod_id.grid(row=0, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Nombre", font=("Arial", 9), bg="white", fg="#475569").grid(row=1, column=0, sticky="w", pady=4)
        self.txt_prod_nombre = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_prod_nombre.grid(row=1, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Precio", font=("Arial", 9), bg="white", fg="#475569").grid(row=2, column=0, sticky="w", pady=4)
        self.txt_prod_precio = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_prod_precio.grid(row=2, column=1, pady=4, padx=(10, 0))

        tk.Label(form_frame, text="Categoría", font=("Arial", 9), bg="white", fg="#475569").grid(row=3, column=0, sticky="w", pady=4)
        self.txt_prod_cat = tk.Entry(form_frame, font=("Arial", 10), bd=1, relief="solid", width=22)
        self.txt_prod_cat.grid(row=3, column=1, pady=4, padx=(10, 0))

        # Botones de productos conectados a sus acciones
        tk.Button(left_frame, text=" Registrar", image=self.icon_add, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", activebackground="#1d4ed8", bd=0, cursor="hand2", anchor="w", padx=12, command=self._registrar_producto_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Cargar por código", image=self.icon_search, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#1e293b", bd=0, cursor="hand2", anchor="w", padx=12, command=self._cargar_producto_por_id).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Actualizar", image=self.icon_edit, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", activebackground="#1d4ed8", bd=0, cursor="hand2", anchor="w", padx=12, command=self._actualizar_producto_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Eliminar", image=self.icon_delete, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#f43f5e", activebackground="#e11d48", bd=0, cursor="hand2", anchor="w", padx=12, command=self._eliminar_producto_accion).pack(fill="x", ipady=5, pady=3)
        tk.Button(left_frame, text=" Limpiar", image=self.icon_clear, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#1e293b", activebackground="#334155", bd=0, cursor="hand2", anchor="w", padx=12, command=self._limpiar_producto_accion).pack(fill="x", ipady=5, pady=3)

        right_frame = tk.LabelFrame(main_container, text=" Productos registrados ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        container_tree = tk.Frame(right_frame, bg="white")
        container_tree.pack(fill="both", expand=True)

        self.tree_productos = ttk.Treeview(container_tree, columns=("ID", "Nombre", "Precio", "Categoría"), show="headings")
        self.tree_productos.heading("ID", text="Código")
        self.tree_productos.heading("Nombre", text="Nombre")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Categoría", text="Categoría")
        
        self.tree_productos.column("ID", width=80, anchor="center")
        self.tree_productos.column("Nombre", width=160, anchor="w")
        self.tree_productos.column("Precio", width=80, anchor="center")
        self.tree_productos.column("Categoría", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(container_tree, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree_productos.bind("<<TreeviewSelect>>", self._cargar_producto_seleccionado)
        self._cargar_tabla_productos()

    def _cargar_tabla_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in self.servicio.obtener_productos():
            self.tree_productos.insert("", "end", values=(p.id, p.nombre, f"${p.precio:.2f}", p.categoria))

    def _limpiar_producto_accion(self):
        self.txt_prod_id.delete(0, tk.END)
        self.txt_prod_nombre.delete(0, tk.END)
        self.txt_prod_precio.delete(0, tk.END)
        self.txt_prod_cat.delete(0, tk.END)

    def _cargar_producto_seleccionado(self, event):
        seleccion = self.tree_productos.selection()
        if seleccion:
            item = self.tree_productos.item(seleccion)
            valores = item['values']
            if valores:
                self.txt_prod_id.delete(0, tk.END)
                self.txt_prod_id.insert(0, valores[0])
                self.txt_prod_nombre.delete(0, tk.END)
                self.txt_prod_nombre.insert(0, valores[1])
                precio_limpio = str(valores[2]).replace("$", "").strip()
                self.txt_prod_precio.delete(0, tk.END)
                self.txt_prod_precio.insert(0, precio_limpio)
                self.txt_prod_cat.delete(0, tk.END)
                self.txt_prod_cat.insert(0, valores[3])

    def _cargar_producto_por_id(self):
        pid = self.txt_prod_id.get().strip()
        if not pid:
            messagebox.showwarning("Atención", "Ingrese el código del producto a buscar.")
            return
        producto = self.servicio.buscar_producto_por_id(pid)
        if producto:
            self.txt_prod_nombre.delete(0, tk.END)
            self.txt_prod_nombre.insert(0, producto.nombre)
            self.txt_prod_precio.delete(0, tk.END)
            self.txt_prod_precio.insert(0, str(producto.precio))
            self.txt_prod_cat.delete(0, tk.END)
            self.txt_prod_cat.insert(0, producto.categoria)
        else:
            messagebox.showerror("No encontrado", f"No existe un producto con el código {pid}.")

    def _registrar_producto_accion(self):
        pid = self.txt_prod_id.get().strip()
        nombre = self.txt_prod_nombre.get().strip()
        precio_str = self.txt_prod_precio.get().strip()
        categoria = self.txt_prod_cat.get().strip()

        if not pid or not nombre or not precio_str or not categoria:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos del producto.")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        exito, mensaje = self.servicio.registrar_producto(pid, nombre, precio, categoria)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._cargar_tabla_productos()
            self._limpiar_producto_accion()
        else:
            messagebox.showerror("Error", mensaje)

    def _actualizar_producto_accion(self):
        pid = self.txt_prod_id.get().strip()
        nombre = self.txt_prod_nombre.get().strip()
        precio_str = self.txt_prod_precio.get().strip()
        categoria = self.txt_prod_cat.get().strip()

        if not pid:
            messagebox.showwarning("Atención", "Ingrese o seleccione el código del producto a actualizar.")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        exito, mensaje = self.servicio.actualizar_producto(pid, nombre, precio, categoria)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._cargar_tabla_productos()
            self._limpiar_producto_accion()
        else:
            messagebox.showerror("Error", mensaje)

    def _eliminar_producto_accion(self):
        pid = self.txt_prod_id.get().strip()
        if not pid:
            messagebox.showwarning("Atención", "Seleccione o ingrese el código del producto a eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {pid}?"):
            exito, mensaje = self.servicio.eliminar_producto(pid)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_tabla_productos()
                self._limpiar_producto_accion()
            else:
                messagebox.showerror("Error", mensaje)

    # ==================== SECCIÓN VENTAS ====================
    def _render_ventas(self):
        tk.Label(self.content_area, text="Ventas", font=("Arial", 18, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w", padx=30, pady=(15, 5))

        main_container = tk.Frame(self.content_area, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=30, pady=10)

        left_frame = tk.Frame(main_container, bg="#f8fafc")
        left_frame.pack(side="left", fill="y", padx=(0, 15))

        form_frame = tk.LabelFrame(left_frame, text=" Registrar venta ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 15))

        tk.Label(form_frame, text="Usuario", font=("Arial", 9), bg="white", fg="#475569").pack(anchor="w", pady=(0, 2))
        self.cbo_usuarios = ttk.Combobox(form_frame, state="readonly", width=28)
        self.cbo_usuarios.pack(pady=(0, 10))

        tk.Label(form_frame, text="Producto", font=("Arial", 9), bg="white", fg="#475569").pack(anchor="w", pady=(0, 2))
        self.cbo_productos = ttk.Combobox(form_frame, state="readonly", width=28)
        self.cbo_productos.pack(pady=(0, 15))

        self.cbo_usuarios['values'] = [f"{u.id} - {u.nombre}" for u in self.servicio.obtener_usuarios()]
        self.cbo_productos['values'] = [f"{p.id} - {p.nombre}" for p in self.servicio.obtener_productos()]

        btn_registrar = tk.Button(
            form_frame, text="+ Registrar venta", font=("Arial", 10, "bold"),
            fg="white", bg="#2563eb", activebackground="#1d4ed8", activeforeground="white",
            bd=0, cursor="hand2", padx=15, pady=6, command=self._callback_registrar_venta
        )
        btn_registrar.pack(fill="x", pady=5)

        right_frame = tk.LabelFrame(main_container, text=" Ventas registradas ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        container_tree = tk.Frame(right_frame, bg="white")
        container_tree.pack(fill="both", expand=True)

        self.tree_ventas = ttk.Treeview(container_tree, columns=("ID", "Usuario", "Producto", "Fecha", "Total"), show="headings")
        self.tree_ventas.heading("ID", text="Venta")
        self.tree_ventas.heading("Usuario", text="Usuario")
        self.tree_ventas.heading("Producto", text="Producto")
        self.tree_ventas.heading("Fecha", text="Fecha")
        self.tree_ventas.heading("Total", text="Total")

        self.tree_ventas.column("ID", width=60, anchor="center")
        self.tree_ventas.column("Usuario", width=110, anchor="w")
        self.tree_ventas.column("Producto", width=110, anchor="w")
        self.tree_ventas.column("Fecha", width=100, anchor="center")
        self.tree_ventas.column("Total", width=70, anchor="center")

        scrollbar = ttk.Scrollbar(container_tree, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)

        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._cargar_tabla_ventas()

    def _callback_registrar_venta(self):
        str_user = self.cbo_usuarios.get()
        str_prod = self.cbo_productos.get()

        if not str_user or not str_prod:
            messagebox.showwarning("Atención", "Por favor seleccione un usuario y un producto.")
            return

        id_usuario = str_user.split(" - ")[0]
        id_producto = str_prod.split(" - ")[0]

        exito, mensaje = self.servicio.registrar_venta(id_usuario, id_producto)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.mostrar_seccion("ventas")
        else:
            messagebox.showerror("Error", mensaje)

    def _cargar_tabla_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        for v in self.servicio.obtener_ventas():
            self.tree_ventas.insert("", "end", values=(v.id, v.usuario_id, v.producto_id, v.fecha, f"${v.total:.2f}"))