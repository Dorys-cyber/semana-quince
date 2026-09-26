import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginView(tk.Tk):
    def __init__(self, servicio, on_login_success):
        super().__init__()
        self.servicio = servicio
        self.on_login_success = on_login_success

        self.title("Restaurante TorVar - Tkinter")
        self.geometry("700x580")
        self.configure(bg="#f1f5f9")
        self.resizable(False, False)

        self.logo_img = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        card = tk.Frame(self, bg="white", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=500)

        # Ruta hacia assets/logo.png
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo = os.path.join(ruta_base, 'assets', 'logo.png')

        if os.path.exists(ruta_logo):
            try:
                img_pil = Image.open(ruta_logo)
                img_pil = img_pil.resize((220, 140), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img_pil)

                lbl_logo = tk.Label(card, image=self.logo_img, bg="white")
                lbl_logo.pack(pady=(20, 10))
            except Exception as e:
                print(f"Error cargando logo: {e}")

        # Título principal "Restaurante" y subtítulo "Inicio de sesión"
        tk.Label(card, text="Restaurante", font=("Arial", 20, "bold"), fg="#0f172a", bg="white").pack(pady=(0, 2))
        tk.Label(card, text="Inicio de sesión", font=("Arial", 11), fg="#64748b", bg="white").pack(pady=(0, 15))

        # Campo Usuario
        frame_user = tk.Frame(card, bg="white")
        frame_user.pack(fill="x", padx=40, pady=6)
        tk.Label(frame_user, text="Usuario", font=("Arial", 10, "bold"), fg="#334155", bg="white").pack(anchor="w")
        self.txt_user = tk.Entry(frame_user, font=("Arial", 11), bd=1, relief="solid")
        self.txt_user.pack(fill="x", ipady=6, pady=(4, 0))

        # Campo Contraseña
        frame_pass = tk.Frame(card, bg="white")
        frame_pass.pack(fill="x", padx=40, pady=6)
        tk.Label(frame_pass, text="Contraseña", font=("Arial", 10, "bold"), fg="#334155", bg="white").pack(anchor="w")
        self.txt_pass = tk.Entry(frame_pass, font=("Arial", 11), show="*", bd=1, relief="solid")
        self.txt_pass.pack(fill="x", ipady=6, pady=(4, 0))

        # Botón Iniciar sesión
        btn_login = tk.Button(
            card, text="Iniciar sesión", font=("Arial", 11, "bold"),
            fg="white", bg="#0284c7", activebackground="#0369a1", activeforeground="white",
            bd=0, cursor="hand2", command=self._callback_login
        )
        btn_login.pack(fill="x", padx=40, ipady=8, pady=(20, 0))

    def _callback_login(self):
        username = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        usuario = self.servicio.autenticar_usuario(username, password)
        if usuario:
            self.destroy()
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")