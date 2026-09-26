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

        self._configurar_estilos()
        self._crear_interfaz()
        self.mostrar_seccion("inicio")

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
        self.btn_inicio = self._crear_boton_sidebar(" Inicio", lambda: self.mostrar_seccion("inicio"))
        self.btn_usuarios = self._crear_boton_sidebar(" Usuarios", lambda: self.mostrar_seccion("usuarios"))
        self.btn_productos = self._crear_boton_sidebar(" Productos", lambda: self.mostrar_seccion("productos"))
        self.btn_ventas = self._crear_boton_sidebar(" Ventas", lambda: self.mostrar_seccion("ventas"))

        # Botón Cerrar sesión
        btn_logout = tk.Button(
            self.sidebar, text=" Cerrar sesión", font=("Arial", 10, "bold"),
            fg="white", bg="#f43f5e", activebackground="#e11d48", activeforeground="white",
            bd=0, anchor="w", padx=20, cursor="hand2", command=self._callback_logout
        )
        btn_logout.pack(side="bottom", fill="x", ipady=10, padx=15, pady=20)

        # 3. Área de Contenido Principal
        self.content_area = tk.Frame(self, bg="#f8fafc")
        self.content_area.pack(side="right", expand=True, fill="both")

    def _callback_logout(self):
        self.destroy()
        if self.on_logout:
            self.on_logout()

    def _crear_boton_sidebar(self, texto, comando):
        btn = tk.Button(
            self.sidebar, text=texto, font=("Arial", 11),
            fg="#e2e8f0", bg="#1e293b", activebackground="#2563eb", activeforeground="white",
            bd=0, anchor="w", padx=20, cursor="hand2", command=comando
        )
        btn.pack(fill="x", ipady=10, pady=2)
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

    def _render_usuarios(self):
        tk.Label(self.content_area, text="Usuarios registrados", font=("Arial", 18, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w", padx=30, pady=(15, 5))
        
        frame_tabla = tk.LabelFrame(self.content_area, text=" Consulta de usuarios ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=15, pady=15)
        frame_tabla.pack(fill="both", expand=True, padx=30, pady=10)

        container_tree = tk.Frame(frame_tabla, bg="white")
        container_tree.pack(fill="both", expand=True)

        tree = ttk.Treeview(container_tree, columns=("ID", "Nombre", "Username", "Rol"), show="headings")
        tree.heading("ID", text="Identificador")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Username", text="Usuario")
        tree.heading("Rol", text="Rol")

        tree.column("ID", width=120, anchor="center")
        tree.column("Nombre", width=180, anchor="w")
        tree.column("Username", width=150, anchor="w")
        tree.column("Rol", width=120, anchor="w")

        scrollbar = ttk.Scrollbar(container_tree, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for u in self.servicio.obtener_usuarios():
            tree.insert("", "end", values=(u.id, u.nombre, u.username, u.rol))

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

        def cargar_icono(nombre):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            ruta = os.path.join(base_dir, "..", "assets", "icons", nombre)
            if os.path.exists(ruta):
                try:
                    if EXIS_PIL:
                        img = Image.open(ruta)
                        img = img.resize((18, 18), Image.Resampling.LANCZOS)
                        return ImageTk.PhotoImage(img)
                    else:
                        return tk.PhotoImage(file=ruta)
                except Exception as e:
                    print(f"Error cargando {nombre}: {e}")
            return None

        self.img_add = cargar_icono("add.png")
        self.img_search = cargar_icono("search.png")
        self.img_edit = cargar_icono("edit.png")
        self.img_delete = cargar_icono("delete.png")
        self.img_clean = cargar_icono("clean.png")

        tk.Button(left_frame, text="   Registrar", image=self.img_add, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", bd=0, cursor="hand2", anchor="w", padx=15).pack(fill="x", ipady=7, pady=3)
        tk.Button(left_frame, text="   Cargar por código", image=self.img_search, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#1e293b", bd=0, cursor="hand2", anchor="w", padx=15).pack(fill="x", ipady=7, pady=3)
        tk.Button(left_frame, text="   Actualizar", image=self.img_edit, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#2563eb", bd=0, cursor="hand2", anchor="w", padx=15).pack(fill="x", ipady=7, pady=3)
        tk.Button(left_frame, text="   Eliminar", image=self.img_delete, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#f43f5e", bd=0, cursor="hand2", anchor="w", padx=15).pack(fill="x", ipady=7, pady=3)
        tk.Button(left_frame, text="   Limpiar", image=self.img_clean, compound="left", font=("Arial", 10, "bold"), fg="white", bg="#1e293b", bd=0, cursor="hand2", anchor="w", padx=15).pack(fill="x", ipady=7, pady=3)

        right_frame = tk.LabelFrame(main_container, text=" Productos registrados ", font=("Arial", 10, "bold"), bg="white", fg="#1e293b", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        container_tree = tk.Frame(right_frame, bg="white")
        container_tree.pack(fill="both", expand=True)

        tree = ttk.Treeview(container_tree, columns=("ID", "Nombre", "Precio", "Categoría"), show="headings")
        tree.heading("ID", text="Código")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio")
        tree.heading("Categoría", text="Categoría")
        
        tree.column("ID", width=80, anchor="center")
        tree.column("Nombre", width=160, anchor="w")
        tree.column("Precio", width=80, anchor="center")
        tree.column("Categoría", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(container_tree, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for p in self.servicio.obtener_productos():
            tree.insert("", "end", values=(p.id, p.nombre, f"${p.precio:.2f}", p.categoria))

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