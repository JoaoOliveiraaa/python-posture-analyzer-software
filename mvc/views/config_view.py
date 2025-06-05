import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import json
import os

class ConfigView:
    def __init__(self, controller):
        self.window = ctk.CTkToplevel()
        self.window.geometry("800x600")
        self.window.title("Configurações - Sistema de Análise de Postura")
        self.controller = controller
        self.window.withdraw()  # Começa oculta

        # Carregar configurações
        self.config_file = "config.json"
        self.config = self._carregar_configuracoes()

        # Criar frames principais
        self._criar_frame_topo()
        self._criar_frame_principal()

    def _carregar_configuracoes(self):
        """Carrega as configurações do arquivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self._configuracoes_padrao()
        return self._configuracoes_padrao()

    def _configuracoes_padrao(self):
        """Retorna as configurações padrão"""
        return {
            "camera": {
                "index": 0,
                "resolucao": "640x480"
            },
            "alerta": {
                "sonoro": True,
                "visual": True,
                "intervalo": 30
            },
            "postura": {
                "angulo_ombro_min": 80,
                "angulo_ombro_max": 100,
                "angulo_quadril_min": 85,
                "angulo_quadril_max": 95
            },
            "interface": {
                "tema": "dark",
                "fonte": "Helvetica",
                "tamanho_fonte": 12
            }
        }

    def _salvar_configuracoes(self):
        """Salva as configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao salvar configurações: {str(e)}")
            return False

    def _criar_frame_topo(self):
        self.top_frame = ctk.CTkFrame(self.window, height=60)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="Configurações",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(side="left", padx=20)

        # Botões de ação
        self.salvar_button = ctk.CTkButton(
            self.top_frame,
            text="Salvar",
            command=self._salvar
        )
        self.salvar_button.pack(side="right", padx=10)

        self.cancelar_button = ctk.CTkButton(
            self.top_frame,
            text="Cancelar",
            command=self.window.destroy
        )
        self.cancelar_button.pack(side="right", padx=10)

    def _criar_frame_principal(self):
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Notebook para abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Criar abas
        self._criar_aba_camera()
        self._criar_aba_alertas()
        self._criar_aba_postura()
        self._criar_aba_interface()

    def _criar_aba_camera(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Câmera")

        # Configurações de câmera
        ctk.CTkLabel(
            frame,
            text="Índice da Câmera:",
            font=("Helvetica", 12)
        ).place(x=20, y=20)

        self.camera_index = ctk.CTkEntry(frame)
        self.camera_index.insert(0, str(self.config["camera"]["index"]))
        self.camera_index.place(x=150, y=20)

        ctk.CTkLabel(
            frame,
            text="Resolução:",
            font=("Helvetica", 12)
        ).place(x=20, y=60)

        self.resolucao = ctk.CTkComboBox(
            frame,
            values=["640x480", "800x600", "1280x720"],
            variable=tk.StringVar(value=self.config["camera"]["resolucao"])
        )
        self.resolucao.place(x=150, y=60)

    def _criar_aba_alertas(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Alertas")

        # Configurações de alerta
        self.alerta_sonoro = ctk.CTkSwitch(
            frame,
            text="Alerta Sonoro",
            variable=tk.BooleanVar(value=self.config["alerta"]["sonoro"])
        )
        self.alerta_sonoro.place(x=20, y=20)

        self.alerta_visual = ctk.CTkSwitch(
            frame,
            text="Alerta Visual",
            variable=tk.BooleanVar(value=self.config["alerta"]["visual"])
        )
        self.alerta_visual.place(x=20, y=60)

        ctk.CTkLabel(
            frame,
            text="Intervalo de Alerta (segundos):",
            font=("Helvetica", 12)
        ).place(x=20, y=100)

        self.intervalo_alerta = ctk.CTkEntry(frame)
        self.intervalo_alerta.insert(0, str(self.config["alerta"]["intervalo"]))
        self.intervalo_alerta.place(x=250, y=100)

    def _criar_aba_postura(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Postura")

        # Configurações de ângulos
        ctk.CTkLabel(
            frame,
            text="Ângulo dos Ombros:",
            font=("Helvetica", 12)
        ).place(x=20, y=20)

        self.angulo_ombro_min = ctk.CTkEntry(frame)
        self.angulo_ombro_min.insert(0, str(self.config["postura"]["angulo_ombro_min"]))
        self.angulo_ombro_min.place(x=150, y=20)

        self.angulo_ombro_max = ctk.CTkEntry(frame)
        self.angulo_ombro_max.insert(0, str(self.config["postura"]["angulo_ombro_max"]))
        self.angulo_ombro_max.place(x=250, y=20)

        ctk.CTkLabel(
            frame,
            text="Ângulo do Quadril:",
            font=("Helvetica", 12)
        ).place(x=20, y=60)

        self.angulo_quadril_min = ctk.CTkEntry(frame)
        self.angulo_quadril_min.insert(0, str(self.config["postura"]["angulo_quadril_min"]))
        self.angulo_quadril_min.place(x=150, y=60)

        self.angulo_quadril_max = ctk.CTkEntry(frame)
        self.angulo_quadril_max.insert(0, str(self.config["postura"]["angulo_quadril_max"]))
        self.angulo_quadril_max.place(x=250, y=60)

    def _criar_aba_interface(self):
        frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(frame, text="Interface")

        # Configurações de interface
        ctk.CTkLabel(
            frame,
            text="Tema:",
            font=("Helvetica", 12)
        ).place(x=20, y=20)

        self.tema = ctk.CTkComboBox(
            frame,
            values=["dark", "light"],
            variable=tk.StringVar(value=self.config["interface"]["tema"])
        )
        self.tema.place(x=150, y=20)

        ctk.CTkLabel(
            frame,
            text="Fonte:",
            font=("Helvetica", 12)
        ).place(x=20, y=60)

        self.fonte = ctk.CTkComboBox(
            frame,
            values=["Helvetica", "Arial", "Times New Roman"],
            variable=tk.StringVar(value=self.config["interface"]["fonte"])
        )
        self.fonte.place(x=150, y=60)

        ctk.CTkLabel(
            frame,
            text="Tamanho da Fonte:",
            font=("Helvetica", 12)
        ).place(x=20, y=100)

        self.tamanho_fonte = ctk.CTkEntry(frame)
        self.tamanho_fonte.insert(0, str(self.config["interface"]["tamanho_fonte"]))
        self.tamanho_fonte.place(x=150, y=100)

    def _salvar(self):
        """Salva as configurações e fecha a janela"""
        try:
            # Atualizar configurações
            self.config["camera"]["index"] = int(self.camera_index.get())
            self.config["camera"]["resolucao"] = self.resolucao.get()
            
            self.config["alerta"]["sonoro"] = self.alerta_sonoro.get()
            self.config["alerta"]["visual"] = self.alerta_visual.get()
            self.config["alerta"]["intervalo"] = int(self.intervalo_alerta.get())
            
            self.config["postura"]["angulo_ombro_min"] = int(self.angulo_ombro_min.get())
            self.config["postura"]["angulo_ombro_max"] = int(self.angulo_ombro_max.get())
            self.config["postura"]["angulo_quadril_min"] = int(self.angulo_quadril_min.get())
            self.config["postura"]["angulo_quadril_max"] = int(self.angulo_quadril_max.get())
            
            self.config["interface"]["tema"] = self.tema.get()
            self.config["interface"]["fonte"] = self.fonte.get()
            self.config["interface"]["tamanho_fonte"] = int(self.tamanho_fonte.get())

            # Salvar no arquivo
            if self._salvar_configuracoes():
                # Atualizar configurações no controller
                self.controller.atualizar_configuracoes(self.config)
                self.window.destroy()
            else:
                ctk.messagebox.showerror("Erro", "Falha ao salvar configurações")
        except ValueError as e:
            ctk.messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
        except Exception as e:
            ctk.messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}") 