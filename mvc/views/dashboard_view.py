import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from datetime import datetime, timedelta
import customtkinter as ctk

class DashboardView:
    def __init__(self, controller):
        self.window = ctk.CTkToplevel()
        self.window.geometry("1200x800")
        self.window.title("Painel de Controle - Sistema de Análise de Postura")
        self.controller = controller
        self.window.withdraw()  # Começa oculta

        # Configuração de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Criar frames principais
        self._criar_frame_topo()
        self._criar_frame_principal()
        self._criar_frame_estatisticas()
        self._criar_frame_configuracoes()

    def _criar_frame_topo(self):
        self.top_frame = ctk.CTkFrame(self.window, height=60)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="Painel de Controle",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(side="left", padx=20)

        # Botão de tema
        self.theme_button = ctk.CTkButton(
            self.top_frame,
            text="Alternar Tema",
            command=self._alternar_tema
        )
        self.theme_button.pack(side="right", padx=20)

    def _criar_frame_principal(self):
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame para gráficos
        self.graficos_frame = ctk.CTkFrame(self.main_frame)
        self.graficos_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Criar figura para os gráficos
        self.fig = plt.Figure(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graficos_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Criar subplots
        self.ax1 = self.fig.add_subplot(121)  # Gráfico de linha
        self.ax2 = self.fig.add_subplot(122)  # Gráfico de pizza

        # Configurar estilo dos gráficos
        sns.set_style("darkgrid")
        self.fig.patch.set_facecolor('#2b2b2b')
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#2b2b2b')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')

    def _criar_frame_estatisticas(self):
        self.stats_frame = ctk.CTkFrame(self.window)
        self.stats_frame.pack(fill="x", padx=10, pady=5)

        # Labels para estatísticas
        self.stats_labels = {}
        stats = [
            ("Tempo Total", "0h"),
            ("Postura Correta", "0%"),
            ("Alertas", "0"),
            ("Sessões", "0")
        ]

        for i, (label, value) in enumerate(stats):
            frame = ctk.CTkFrame(self.stats_frame)
            frame.pack(side="left", expand=True, padx=10, pady=5)
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=("Helvetica", 12)
            ).pack()
            
            self.stats_labels[label] = ctk.CTkLabel(
                frame,
                text=value,
                font=("Helvetica", 16, "bold")
            )
            self.stats_labels[label].pack()

    def _criar_frame_configuracoes(self):
        self.config_frame = ctk.CTkFrame(self.window)
        self.config_frame.pack(fill="x", padx=10, pady=5)

        # Controles de período
        ctk.CTkLabel(
            self.config_frame,
            text="Período:"
        ).pack(side="left", padx=10)

        self.periodo_var = tk.StringVar(value="7")
        self.periodo_combo = ctk.CTkComboBox(
            self.config_frame,
            values=["7", "15", "30"],
            variable=self.periodo_var,
            command=self._atualizar_graficos
        )
        self.periodo_combo.pack(side="left", padx=10)

        # Botão de atualização
        self.atualizar_button = ctk.CTkButton(
            self.config_frame,
            text="Atualizar",
            command=self._atualizar_graficos
        )
        self.atualizar_button.pack(side="left", padx=10)

    def _alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        if ctk.get_appearance_mode() == "dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def _atualizar_graficos(self, *args):
        """Atualiza os gráficos com os dados mais recentes"""
        try:
            dias = int(self.periodo_var.get())
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=dias)
            
            # Obter dados do controller
            dados = self.controller.model.get_estatisticas_periodo(data_inicio, data_fim)
            
            # Limpar gráficos
            self.ax1.clear()
            self.ax2.clear()
            
            # Gráfico de linha (evolução temporal)
            self.ax1.plot(
                dados['datas'],
                dados['percentuais'],
                marker='o',
                color='#1f77b4'
            )
            self.ax1.set_title('Evolução da Postura')
            self.ax1.set_xlabel('Data')
            self.ax1.set_ylabel('Percentual Correto (%)')
            
            # Gráfico de pizza (distribuição)
            self.ax2.pie(
                [dados['tempo_postura_correta'], dados['tempo_postura_incorreta']],
                labels=['Correta', 'Incorreta'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c']
            )
            self.ax2.set_title('Distribuição da Postura')
            
            # Atualizar canvas
            self.canvas.draw()
            
            # Atualizar estatísticas
            self._atualizar_estatisticas(dados)
            
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar gráficos: {str(e)}")

    def _atualizar_estatisticas(self, dados):
        """Atualiza as estatísticas na interface"""
        self.stats_labels["Tempo Total"].configure(
            text=f"{dados['tempo_total']}h"
        )
        self.stats_labels["Postura Correta"].configure(
            text=f"{dados['percentual_correto']:.1f}%"
        )
        self.stats_labels["Alertas"].configure(
            text=str(dados['total_alertas'])
        )
        self.stats_labels["Sessões"].configure(
            text=str(dados['total_sessoes'])
        ) 