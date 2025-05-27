from views.view import View
from models.model import Model
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple
import time
import winsound
import threading
from datetime import datetime, timedelta

class Controller:
    def __init__(self, model, root):
        self.model = model
        self.view = View(root, self)
        self.cap = None
        self.is_running = False
        self.camera_index = 0
        self.resolution = (640, 480)
        self.fps = 30
        
        # Variáveis para controle de alertas
        self.ultimo_alerta = 0
        self.intervalo_alerta = 5  # segundos entre alertas
        self.alerta_sonoro_ativado = True
        self.tempo_postura_incorreta = 0
        self.tempo_limite_alerta = 10  # segundos em postura incorreta antes do alerta
        
        # Variáveis para estatísticas
        self.tempo_inicio_sessao = None
        self.tempo_postura_correta = 0
        self.tempo_postura_incorreta = 0
        self.total_analises = 0
        
        # Inicializa MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Inicializa thread para alertas sonoros
        self.thread_alerta = None
        self.alerta_rodando = False

        # Iniciar thread de estatísticas
        self.thread_estatisticas = threading.Thread(target=self._atualizar_estatisticas_periodicamente)
        self.thread_estatisticas.daemon = True
        self.thread_estatisticas.start()

    def iniciar_monitoramento(self):
        if not self.is_running:
            try:
                self.cap = cv2.VideoCapture(self.camera_index)
                if self.cap.isOpened():
                    # Configura resolução e FPS
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                    self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                    
                    self.is_running = True
                    self.tempo_postura_incorreta = 0
                    self.tempo_inicio_sessao = time.time()
                    self.atualizar_frame()
                    self.view.atualizar_status("Monitoramento iniciado com sucesso!", "success")
                    print("[INFO] Monitoramento iniciado com sucesso")
                else:
                    self.view.atualizar_status("Erro ao acessar a webcam!", "error")
                    print("[ERRO] Falha ao acessar a webcam")
            except Exception as e:
                self.view.atualizar_status(f"Erro ao iniciar câmera: {str(e)}", "error")
                print(f"[ERRO] Falha ao iniciar câmera: {str(e)}")

    def parar_monitoramento(self):
        self.is_running = False
        self.alerta_rodando = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.view.atualizar_status("Monitoramento parado!", "info")
        print("[INFO] Monitoramento parado")

    def toggle_alerta_sonoro(self):
        """Ativa/desativa alertas sonoros"""
        self.alerta_sonoro_ativado = not self.alerta_sonoro_ativado
        status = "ativado" if self.alerta_sonoro_ativado else "desativado"
        self.view.atualizar_status(f"Alerta sonoro {status}", "info")
        print(f"[INFO] Alerta sonoro {status}")

    def reproduzir_alerta_sonoro(self):
        """Reproduz o alerta sonoro em uma thread separada"""
        if self.alerta_sonoro_ativado and not self.alerta_rodando:
            self.alerta_rodando = True
            self.thread_alerta = threading.Thread(target=self._alerta_sonoro_thread)
            self.thread_alerta.start()

    def _alerta_sonoro_thread(self):
        """Thread para reproduzir o alerta sonoro"""
        try:
            # Frequência e duração do beep
            winsound.Beep(1000, 500)  # 1000Hz por 500ms
            time.sleep(0.5)
            winsound.Beep(1000, 500)
        except Exception as e:
            print(f"[ERRO] Falha ao reproduzir alerta sonoro: {str(e)}")
        finally:
            self.alerta_rodando = False

    def trocar_camera(self, index: int):
        """Troca para uma câmera diferente"""
        if self.is_running:
            self.parar_monitoramento()
        self.camera_index = index
        self.iniciar_monitoramento()

    def alterar_resolucao(self, width: int, height: int):
        """Altera a resolução da câmera"""
        if self.is_running:
            self.parar_monitoramento()
        self.resolution = (width, height)
        self.iniciar_monitoramento()

    def detectar_postura(self, frame) -> Tuple[np.ndarray, Optional[dict]]:
        """Detecta a postura usando MediaPipe"""
        try:
            # Converte para RGB para o MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)
            
            if results.pose_landmarks:
                # Desenha os pontos e conexões
                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                # Extrai coordenadas dos pontos importantes
                landmarks = results.pose_landmarks.landmark
                postura = self.analisar_postura(landmarks)
                
                # Processa alertas se a postura estiver incorreta
                if postura and not postura['postura_correta']:
                    self.processar_alerta_postura_incorreta(postura)
                
                return frame, postura
            
            return frame, None
        except Exception as e:
            print(f"[ERRO] Falha na detecção de postura: {str(e)}")
            return frame, None

    def processar_alerta_postura_incorreta(self, postura: dict):
        """Processa alertas para postura incorreta"""
        tempo_atual = time.time()
        
        # Incrementa o tempo em postura incorreta
        self.tempo_postura_incorreta += 1
        
        # Verifica se deve emitir alerta
        if (self.tempo_postura_incorreta >= self.tempo_limite_alerta and 
            tempo_atual - self.ultimo_alerta >= self.intervalo_alerta):
            
            self.ultimo_alerta = tempo_atual
            self.tempo_postura_incorreta = 0
            
            # Gera sugestão de correção
            sugestao = self.gerar_sugestao_correcao(postura)
            
            # Atualiza interface
            self.view.atualizar_alerta(sugestao)
            
            # Reproduz alerta sonoro
            self.reproduzir_alerta_sonoro()
            
            print(f"[ALERTA] Postura incorreta detectada: {sugestao}")

    def gerar_sugestao_correcao(self, postura: dict) -> str:
        """Gera sugestão de correção baseada na análise da postura"""
        sugestoes = []
        
        if postura['angulo_ombros'] > 5:
            sugestoes.append("Alinhe seus ombros")
        
        if postura['angulo_quadril'] > 5:
            sugestoes.append("Mantenha o quadril nivelado")
        
        if not sugestoes:
            return "Ajuste sua postura para uma posição mais ereta"
        
        return " | ".join(sugestoes)

    def analisar_postura(self, landmarks) -> dict:
        """Analisa a postura baseado nos landmarks do MediaPipe"""
        try:
            # Obtém coordenadas dos pontos importantes
            ombro_esquerdo = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            ombro_direito = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            quadril_esquerdo = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            quadril_direito = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            # Calcula ângulos
            angulo_ombros = self.calcular_angulo(
                ombro_esquerdo, ombro_direito
            )
            angulo_quadril = self.calcular_angulo(
                quadril_esquerdo, quadril_direito
            )
            
            postura_correta = self.verificar_postura_correta(angulo_ombros, angulo_quadril)
            
            # Registra a análise no banco de dados
            self.model.registrar_analise_postura(angulo_ombros, angulo_quadril, postura_correta)
            
            return {
                "angulo_ombros": angulo_ombros,
                "angulo_quadril": angulo_quadril,
                "postura_correta": postura_correta
            }
        except Exception as e:
            print(f"[ERRO] Falha na análise de postura: {str(e)}")
            return None

    def calcular_angulo(self, ponto1, ponto2) -> float:
        """Calcula o ângulo entre dois pontos"""
        return abs(ponto1.y - ponto2.y) * 180

    def verificar_postura_correta(self, angulo_ombros: float, angulo_quadril: float) -> bool:
        """Verifica se a postura está correta baseado nos ângulos"""
        # Valores de referência para postura correta
        return angulo_ombros < 5 and angulo_quadril < 5

    def atualizar_frame(self):
        if self.is_running and self.cap is not None:
            try:
                ret, frame = self.cap.read()
                if ret:
                    # Processa o frame para detecção de postura
                    frame_processado, postura = self.detectar_postura(frame)
                    
                    # Converte o frame para RGB
                    frame_rgb = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2RGB)
                    
                    # Converte para formato PIL
                    image = Image.fromarray(frame_rgb)
                    
                    # Redimensiona mantendo proporção
                    image.thumbnail(self.resolution)
                    
                    # Converte para formato Tkinter
                    photo = ImageTk.PhotoImage(image=image)
                    
                    # Atualiza a view
                    self.view.atualizar_video(photo)
                    if postura:
                        self.view.atualizar_estatisticas(postura)
                
                # Agenda próxima atualização
                self.view.window.after(10, self.atualizar_frame)
            except Exception as e:
                print(f"[ERRO] Falha ao processar frame: {str(e)}")
                self.view.atualizar_status(f"Erro ao processar frame: {str(e)}", "error")
                self.parar_monitoramento() 

    def _atualizar_estatisticas_tempo_real(self, postura):
        """Atualiza estatísticas em tempo real"""
        try:
            if postura['postura_correta']:
                self.tempo_postura_correta += 1/self.fps
            else:
                self.tempo_postura_incorreta += 1/self.fps
            
            self.total_analises += 1
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar estatísticas: {str(e)}")

    def _atualizar_estatisticas_periodicamente(self):
        """Thread para atualizar estatísticas periodicamente"""
        while True:
            try:
                if self.is_running:
                    self._registrar_estatisticas_sessao()
                time.sleep(60)  # Atualizar a cada minuto
            except Exception as e:
                print(f"[ERRO] Falha na atualização periódica de estatísticas: {str(e)}")
                time.sleep(60)

    def _registrar_estatisticas_sessao(self):
        """Registra estatísticas da sessão atual"""
        try:
            if self.tempo_inicio_sessao is not None:
                duracao = time.time() - self.tempo_inicio_sessao
                
                # Registrar no banco de dados
                self.model.registrar_analise_postura(
                    angulo_ombros=0,  # Valores médios serão calculados pelo modelo
                    angulo_quadril=0,
                    postura_correta=True,
                    duracao=duracao
                )
                
                # Resetar contadores
                self.tempo_postura_correta = 0
                self.tempo_postura_incorreta = 0
                self.total_analises = 0
                self.tempo_inicio_sessao = time.time()
                
                print("[INFO] Estatísticas da sessão registradas")
        except Exception as e:
            print(f"[ERRO] Falha ao registrar estatísticas da sessão: {str(e)}") 