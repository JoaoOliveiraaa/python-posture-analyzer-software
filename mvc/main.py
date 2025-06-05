import tkinter as tk
from models.model import Model
from controllers.controller import Controller
from views.view import View
from views.dashboard_view import DashboardView
from views.config_view import ConfigView
import customtkinter as ctk

def main():
    # Configurar tema padrão
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Criar janela principal
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("Sistema de Análise de Postura")

    # Criar modelo e controlador
    model = Model()
    controller = Controller(model)

    # Criar view principal
    view = View(root, controller)
    controller.set_view(view)

    # Criar janelas secundárias (iniciam ocultas)
    dashboard = DashboardView(controller)
    config = ConfigView(controller)

    # Funções para mostrar as janelas
    def abrir_dashboard():
        dashboard.window.deiconify()
        dashboard.window.lift()

    def abrir_config():
        config.window.deiconify()
        config.window.lift()

    # Configurar menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Menu Arquivo
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Arquivo", menu=file_menu)
    file_menu.add_command(label="Configurações", command=abrir_config)
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    # Menu Visualização
    view_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Visualização", menu=view_menu)
    view_menu.add_command(label="Painel de Controle", command=abrir_dashboard)
    view_menu.add_command(label="Monitoramento", command=lambda: root.deiconify())

    # Iniciar aplicação
    root.mainloop()

if __name__ == "__main__":
    main() 