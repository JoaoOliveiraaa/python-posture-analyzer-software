import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta

class View:
    def __init__(self, root, controller):
        self.window = root
        self.controller = controller
        self.window.geometry("1024x768")
        self.window.title("Sistema de Análise de Postura")

        # Configuração de estilos
        self.style = ttk.Style()
        self.style.configure('Cinza.TFrame', background='#4F4F4F')
        self.style.configure('BrancoTexto.TLabel', background='#4F4F4F', foreground='white')
        self.style.configure('Status.TLabel', font=('Helvetica', 10))
        self.style.configure('Alerta.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Sugestao.TLabel', font=('Helvetica', 11))
        self.style.configure('Estatistica.TLabel', font=('Helvetica', 10))

        # Criar frames
        self._criar_frame_topo()
        self._criar_frame_principal()
        self._criar_frame_controles()
        self._criar_frame_estatisticas()
        self._criar_frame_rodape()

    def _criar_frame_topo(self):
        self.top_frame = ttk.Frame(self.window, height=50, style='Cinza.TFrame')
        self.top_frame.pack(fill="x", padx=1, pady=1)
        self.top_frame.pack_propagate(False)
        
        self.title_label = ttk.Label(self.top_frame,
                                   text="Sistema de Análise de Postura",
                                   font=("Helvetica", 16, "bold"),
                                   style='BrancoTexto.TLabel')
        self.title_label.place(x=20, y=10)

        # Label para status
        self.status_label = ttk.Label(self.top_frame,
                                    text="Sistema pronto",
                                    style='Status.TLabel')
        self.status_label.place(x=700, y=15)

    def _criar_frame_principal(self):
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(padx=1, pady=1, fill="both", expand=True)
        
        # Frame para vídeo
        self.video_frame = ttk.LabelFrame(self.main_frame, text="Visualização")
        self.video_frame.place(x=20, y=20, width=640, height=480)
        
        # Área para exibir o vídeo
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.place(x=10, y=10)

        # Frame para estatísticas
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Estatísticas de Postura")
        self.stats_frame.place(x=680, y=20, width=300, height=200)

        # Labels para estatísticas
        self.angulo_ombros_label = ttk.Label(self.stats_frame, text="Ângulo dos Ombros: --")
        self.angulo_ombros_label.place(x=10, y=20)

        self.angulo_quadril_label = ttk.Label(self.stats_frame, text="Ângulo do Quadril: --")
        self.angulo_quadril_label.place(x=10, y=50)

        self.postura_label = ttk.Label(self.stats_frame, text="Status da Postura: --")
        self.postura_label.place(x=10, y=80)

        # Frame para alertas
        self.alerta_frame = ttk.LabelFrame(self.main_frame, text="Alertas e Sugestões")
        self.alerta_frame.place(x=680, y=240, width=300, height=150)

        # Label para alerta
        self.alerta_label = ttk.Label(self.alerta_frame,
                                    text="Nenhum alerta",
                                    style='Alerta.TLabel')
        self.alerta_label.place(x=10, y=10)

        # Label para sugestão
        self.sugestao_label = ttk.Label(self.alerta_frame,
                                      text="",
                                      style='Sugestao.TLabel',
                                      wraplength=280)
        self.sugestao_label.place(x=10, y=40)

    def _criar_frame_controles(self):
        self.controles_frame = ttk.LabelFrame(self.main_frame, text="Controles")
        self.controles_frame.place(x=680, y=400, width=300, height=200)

        # Controle de câmera
        ttk.Label(self.controles_frame, text="Câmera:").place(x=10, y=20)
        self.camera_var = tk.StringVar(value="0")
        self.camera_combo = ttk.Combobox(self.controles_frame, 
                                       textvariable=self.camera_var,
                                       values=["0", "1", "2"],
                                       width=5)
        self.camera_combo.place(x=70, y=20)
        self.camera_combo.bind('<<ComboboxSelected>>', self._on_camera_change)

        # Controle de resolução
        ttk.Label(self.controles_frame, text="Resolução:").place(x=10, y=50)
        self.resolucao_var = tk.StringVar(value="640x480")
        self.resolucao_combo = ttk.Combobox(self.controles_frame,
                                          textvariable=self.resolucao_var,
                                          values=["640x480", "800x600", "1280x720"],
                                          width=10)
        self.resolucao_combo.place(x=70, y=50)
        self.resolucao_combo.bind('<<ComboboxSelected>>', self._on_resolucao_change)

        # Controle de alerta sonoro
        self.alerta_sonoro_var = tk.BooleanVar(value=True)
        self.alerta_sonoro_check = ttk.Checkbutton(
            self.controles_frame,
            text="Alerta Sonoro",
            variable=self.alerta_sonoro_var,
            command=self._on_alerta_sonoro_change
        )
        self.alerta_sonoro_check.place(x=10, y=80)

    def _criar_frame_estatisticas(self):
        self.estatisticas_frame = ttk.LabelFrame(self.main_frame, text="Estatísticas e Exportação")
        self.estatisticas_frame.place(x=20, y=520, width=960, height=200)

        # Frame para estatísticas diárias
        self.estatisticas_diarias_frame = ttk.Frame(self.estatisticas_frame)
        self.estatisticas_diarias_frame.place(x=10, y=10, width=300, height=180)

        # Labels para estatísticas diárias
        self.tempo_correto_label = ttk.Label(self.estatisticas_diarias_frame,
                                           text="Tempo Postura Correta: --",
                                           style='Estatistica.TLabel')
        self.tempo_correto_label.place(x=10, y=10)

        self.tempo_incorreto_label = ttk.Label(self.estatisticas_diarias_frame,
                                             text="Tempo Postura Incorreta: --",
                                             style='Estatistica.TLabel')
        self.tempo_incorreto_label.place(x=10, y=40)

        self.total_analises_label = ttk.Label(self.estatisticas_diarias_frame,
                                            text="Total de Análises: --",
                                            style='Estatistica.TLabel')
        self.total_analises_label.place(x=10, y=70)

        self.percentual_label = ttk.Label(self.estatisticas_diarias_frame,
                                        text="Percentual Correto: --",
                                        style='Estatistica.TLabel')
        self.percentual_label.place(x=10, y=100)

        # Frame para exportação
        self.exportacao_frame = ttk.Frame(self.estatisticas_frame)
        self.exportacao_frame.place(x=320, y=10, width=300, height=180)

        # Botões de exportação
        self.botao_exportar_csv = ttk.Button(self.exportacao_frame,
                                           text="Exportar CSV",
                                           command=self._exportar_csv)
        self.botao_exportar_csv.place(x=10, y=10)

        self.botao_exportar_json = ttk.Button(self.exportacao_frame,
                                            text="Exportar JSON",
                                            command=self._exportar_json)
        self.botao_exportar_json.place(x=10, y=50)

        # Frame para período
        self.periodo_frame = ttk.Frame(self.estatisticas_frame)
        self.periodo_frame.place(x=640, y=10, width=300, height=180)

        # Controles de período
        ttk.Label(self.periodo_frame, text="Período:").place(x=10, y=10)
        self.periodo_var = tk.StringVar(value="7")
        self.periodo_combo = ttk.Combobox(self.periodo_frame,
                                        textvariable=self.periodo_var,
                                        values=["7", "15", "30"],
                                        width=5)
        self.periodo_combo.place(x=70, y=10)
        self.periodo_combo.bind('<<ComboboxSelected>>', self._on_periodo_change)

        # Botão para atualizar estatísticas
        self.botao_atualizar = ttk.Button(self.periodo_frame,
                                        text="Atualizar Estatísticas",
                                        command=self._atualizar_estatisticas)
        self.botao_atualizar.place(x=10, y=50)

    def _criar_frame_rodape(self):
        self.bottom_frame = ttk.Frame(self.window, height=50, style='Cinza.TFrame')
        self.bottom_frame.pack(fill="x", padx=1, pady=1, side="bottom")
        self.bottom_frame.pack_propagate(False)
        
        self.botao_iniciar = ttk.Button(self.bottom_frame, 
                                      text="Iniciar Monitoramento",
                                      command=self.controller.iniciar_monitoramento)
        self.botao_iniciar.place(x=20, y=10)

        self.botao_parar = ttk.Button(self.bottom_frame,
                                    text="Parar Monitoramento",
                                    command=self.controller.parar_monitoramento)
        self.botao_parar.place(x=200, y=10)

    def _on_camera_change(self, event):
        try:
            index = int(self.camera_var.get())
            self.controller.trocar_camera(index)
        except ValueError:
            messagebox.showerror("Erro", "Valor de câmera inválido")

    def _on_resolucao_change(self, event):
        try:
            width, height = map(int, self.resolucao_var.get().split('x'))
            self.controller.alterar_resolucao(width, height)
        except ValueError:
            messagebox.showerror("Erro", "Formato de resolução inválido")

    def _on_alerta_sonoro_change(self):
        """Callback para mudança no estado do alerta sonoro"""
        self.controller.toggle_alerta_sonoro()

    def _on_periodo_change(self, event):
        """Callback para mudança no período de estatísticas"""
        self._atualizar_estatisticas()

    def _atualizar_estatisticas(self):
        """Atualiza as estatísticas na interface"""
        try:
            dias = int(self.periodo_var.get())
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=dias)
            
            estatisticas = self.controller.model.get_estatisticas_periodo(data_inicio, data_fim)
            
            self.tempo_correto_label.configure(
                text=f"Tempo Postura Correta: {estatisticas['tempo_postura_correta']}s"
            )
            self.tempo_incorreto_label.configure(
                text=f"Tempo Postura Incorreta: {estatisticas['tempo_postura_incorreta']}s"
            )
            self.total_analises_label.configure(
                text=f"Total de Análises: {estatisticas['total_analises']}"
            )
            self.percentual_label.configure(
                text=f"Percentual Correto: {estatisticas['percentual_correto']:.1f}%"
            )
            
            print(f"[INFO] Estatísticas atualizadas para o período de {dias} dias")
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar estatísticas: {str(e)}")
            messagebox.showerror("Erro", "Falha ao atualizar estatísticas")

    def _exportar_csv(self):
        """Exporta os dados para CSV"""
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv")],
                title="Exportar para CSV"
            )
            
            if caminho:
                dias = int(self.periodo_var.get())
                if self.controller.model.exportar_dados_csv(caminho, dias):
                    messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha ao exportar dados")
        except Exception as e:
            print(f"[ERRO] Falha ao exportar CSV: {str(e)}")
            messagebox.showerror("Erro", "Falha ao exportar dados")

    def _exportar_json(self):
        """Exporta os dados para JSON"""
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Arquivos JSON", "*.json")],
                title="Exportar para JSON"
            )
            
            if caminho:
                dias = int(self.periodo_var.get())
                if self.controller.model.exportar_dados_json(caminho, dias):
                    messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha ao exportar dados")
        except Exception as e:
            print(f"[ERRO] Falha ao exportar JSON: {str(e)}")
            messagebox.showerror("Erro", "Falha ao exportar dados")

    def atualizar_video(self, photo):
        """Atualiza o frame do vídeo na interface"""
        self.video_label.configure(image=photo)
        self.video_label.image = photo

    def atualizar_estatisticas(self, postura):
        """Atualiza as estatísticas de postura na interface"""
        self.angulo_ombros_label.configure(
            text=f"Ângulo dos Ombros: {postura['angulo_ombros']:.1f}°"
        )
        self.angulo_quadril_label.configure(
            text=f"Ângulo do Quadril: {postura['angulo_quadril']:.1f}°"
        )
        status = "Correta" if postura['postura_correta'] else "Incorreta"
        cor = "green" if postura['postura_correta'] else "red"
        self.postura_label.configure(
            text=f"Status da Postura: {status}",
            foreground=cor
        )

    def atualizar_alerta(self, sugestao: str):
        """Atualiza o alerta e sugestão na interface"""
        self.alerta_label.configure(
            text="⚠️ Postura Incorreta Detectada!",
            foreground="red"
        )
        self.sugestao_label.configure(
            text=sugestao,
            foreground="blue"
        )
        
        # Agenda a limpeza do alerta após 5 segundos
        self.window.after(5000, self.limpar_alerta)

    def limpar_alerta(self):
        """Limpa o alerta e sugestão da interface"""
        self.alerta_label.configure(
            text="Nenhum alerta",
            foreground="black"
        )
        self.sugestao_label.configure(
            text="",
            foreground="black"
        )

    def atualizar_status(self, mensagem: str, tipo: str = "info"):
        """Atualiza a mensagem de status na interface"""
        cores = {
            "success": "green",
            "error": "red",
            "info": "white"
        }
        self.status_label.configure(
            text=mensagem,
            foreground=cores.get(tipo, "white")
        ) 