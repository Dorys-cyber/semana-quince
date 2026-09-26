from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

def iniciar_app():
    servicio = RestauranteServicio()

    def mostrar_login():
        def abrir_main_view(usuario):
            # Ya no llamamos a login.destroy() aquí porque LoginView ya se destruye solo
            app_main = MainView(servicio, usuario, on_logout=mostrar_login)
            app_main.mainloop()

        login = LoginView(servicio, abrir_main_view)
        login.mainloop()

    mostrar_login()

if __name__ == "__main__":
    iniciar_app()