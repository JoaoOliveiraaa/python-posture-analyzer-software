import mysql.connector
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import csv
import json
import os

class Model:
    def __init__(self):
        # Configurações do MySQL para WAMP
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Senha padrão do WAMP é vazia
            'database': 'postura_db',
            'port': 3306  # Porta padrão do MySQL no WAMP
        }
        
        try:
            # Primeiro, conectar sem especificar o banco de dados
            self.conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config['port']
            )
            
            cursor = self.conn.cursor()
            
            # Verificar se o banco de dados existe
            cursor.execute("SHOW DATABASES LIKE 'postura_db'")
            if not cursor.fetchone():
                print("[INFO] Banco de dados não encontrado. Criando banco de dados...")
                cursor.execute("CREATE DATABASE postura_db")
                print("[INFO] Banco de dados criado com sucesso!")
            
            # Usar o banco de dados
            cursor.execute("USE postura_db")
            self.conn.commit()
            
            print("[INFO] Conexão com MySQL estabelecida com sucesso")
            self.criar_tabelas()
            
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("[ERRO] Erro de acesso: usuário ou senha incorretos")
                print("[INFO] Verifique se o WAMP está rodando e se as credenciais estão corretas")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("[ERRO] Banco de dados não existe")
            else:
                print(f"[ERRO] Erro ao conectar ao MySQL: {err}")
            raise

    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        try:
            cursor = self.conn.cursor()
            
            # Tabela de registros de postura
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_postura (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data_hora DATETIME NOT NULL,
                    angulo_ombros FLOAT NOT NULL,
                    angulo_quadril FLOAT NOT NULL,
                    postura_correta BOOLEAN NOT NULL,
                    duracao FLOAT
                )
            ''')
            
            # Tabela de estatísticas diárias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estatisticas_diarias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data DATE NOT NULL,
                    tempo_postura_correta FLOAT NOT NULL,
                    tempo_postura_incorreta FLOAT NOT NULL,
                    total_analises INT NOT NULL,
                    media_angulo_ombros FLOAT,
                    media_angulo_quadril FLOAT,
                    UNIQUE(data)
                )
            ''')
            
            self.conn.commit()
            print("[INFO] Tabelas criadas com sucesso")
        except Exception as e:
            print(f"[ERRO] Falha ao criar tabelas: {str(e)}")
            raise

    def registrar_analise_postura(self, angulo_ombros: float, angulo_quadril: float, 
                                postura_correta: bool, duracao: Optional[float] = None):
        """Registra uma análise de postura no banco de dados"""
        try:
            cursor = self.conn.cursor()
            
            # Registrar análise
            cursor.execute('''
                INSERT INTO registros_postura 
                (data_hora, angulo_ombros, angulo_quadril, postura_correta, duracao)
                VALUES (%s, %s, %s, %s, %s)
            ''', (datetime.now(), angulo_ombros, angulo_quadril, postura_correta, duracao))
            
            # Atualizar estatísticas diárias
            self._atualizar_estatisticas_diarias(angulo_ombros, angulo_quadril, postura_correta, duracao)
            
            self.conn.commit()
            print(f"[INFO] Análise registrada - Postura: {'Correta' if postura_correta else 'Incorreta'}")
        except Exception as e:
            print(f"[ERRO] Falha ao registrar análise: {str(e)}")
            self.conn.rollback()
            raise

    def _atualizar_estatisticas_diarias(self, angulo_ombros: float, angulo_quadril: float,
                                      postura_correta: bool, duracao: Optional[float] = None):
        """Atualiza as estatísticas diárias com base na análise"""
        try:
            cursor = self.conn.cursor()
            data_atual = datetime.now().date()
            
            # Verificar se já existe registro para hoje
            cursor.execute('''
                SELECT id, tempo_postura_correta, tempo_postura_incorreta, total_analises,
                       media_angulo_ombros, media_angulo_quadril
                FROM estatisticas_diarias
                WHERE data = %s
            ''', (data_atual,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Atualizar estatísticas existentes
                id_estatistica, tempo_correto, tempo_incorreto, total, media_ombros, media_quadril = resultado
                
                if duracao:
                    if postura_correta:
                        tempo_correto += duracao
                    else:
                        tempo_incorreto += duracao
                else:
                    if postura_correta:
                        tempo_correto += 1
                    else:
                        tempo_incorreto += 1
                
                total += 1
                
                # Atualizar médias
                media_ombros = ((media_ombros * (total - 1)) + angulo_ombros) / total
                media_quadril = ((media_quadril * (total - 1)) + angulo_quadril) / total
                
                cursor.execute('''
                    UPDATE estatisticas_diarias
                    SET tempo_postura_correta = %s,
                        tempo_postura_incorreta = %s,
                        total_analises = %s,
                        media_angulo_ombros = %s,
                        media_angulo_quadril = %s
                    WHERE id = %s
                ''', (tempo_correto, tempo_incorreto, total, media_ombros, media_quadril, id_estatistica))
            else:
                # Criar novo registro
                tempo_correto = duracao if postura_correta and duracao else (1 if postura_correta else 0)
                tempo_incorreto = duracao if not postura_correta and duracao else (1 if not postura_correta else 0)
                
                cursor.execute('''
                    INSERT INTO estatisticas_diarias
                    (data, tempo_postura_correta, tempo_postura_incorreta, total_analises,
                     media_angulo_ombros, media_angulo_quadril)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (data_atual, tempo_correto, tempo_incorreto, 1, angulo_ombros, angulo_quadril))
            
            self.conn.commit()
            print("[INFO] Estatísticas diárias atualizadas")
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar estatísticas diárias: {str(e)}")
            self.conn.rollback()
            raise

    def get_estatisticas_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict:
        """Obtém estatísticas para um período específico"""
        try:
            cursor = self.conn.cursor()
            
            # Obter estatísticas gerais
            cursor.execute('''
                SELECT SUM(tempo_postura_correta) as tempo_correto,
                       SUM(tempo_postura_incorreta) as tempo_incorreto,
                       SUM(total_analises) as total,
                       AVG(media_angulo_ombros) as media_ombros,
                       AVG(media_angulo_quadril) as media_quadril,
                       COUNT(DISTINCT data) as total_sessoes
                FROM estatisticas_diarias
                WHERE data BETWEEN %s AND %s
            ''', (data_inicio.date(), data_fim.date()))
            
            resultado = cursor.fetchone()
            
            # Obter dados para gráfico de evolução
            cursor.execute('''
                SELECT data,
                       (tempo_postura_correta / (tempo_postura_correta + tempo_postura_incorreta) * 100) as percentual
                FROM estatisticas_diarias
                WHERE data BETWEEN %s AND %s
                ORDER BY data ASC
            ''', (data_inicio.date(), data_fim.date()))
            
            evolucao = cursor.fetchall()
            
            # Obter total de alertas
            cursor.execute('''
                SELECT COUNT(*) as total_alertas
                FROM registros_postura
                WHERE data_hora BETWEEN %s AND %s
                AND postura_correta = FALSE
            ''', (data_inicio, data_fim))
            
            total_alertas = cursor.fetchone()[0]
            
            if resultado:
                tempo_correto, tempo_incorreto, total, media_ombros, media_quadril, total_sessoes = resultado
                tempo_total = tempo_correto + tempo_incorreto
                percentual = (tempo_correto / tempo_total * 100) if tempo_total > 0 else 0
                
                return {
                    'tempo_postura_correta': tempo_correto or 0,
                    'tempo_postura_incorreta': tempo_incorreto or 0,
                    'total_analises': total or 0,
                    'media_angulo_ombros': media_ombros or 0,
                    'media_angulo_quadril': media_quadril or 0,
                    'percentual_correto': percentual,
                    'total_sessoes': total_sessoes or 0,
                    'total_alertas': total_alertas,
                    'datas': [row[0] for row in evolucao],
                    'percentuais': [row[1] for row in evolucao]
                }
            
            return {
                'tempo_postura_correta': 0,
                'tempo_postura_incorreta': 0,
                'total_analises': 0,
                'media_angulo_ombros': 0,
                'media_angulo_quadril': 0,
                'percentual_correto': 0,
                'total_sessoes': 0,
                'total_alertas': 0,
                'datas': [],
                'percentuais': []
            }
        except Exception as e:
            print(f"[ERRO] Falha ao obter estatísticas do período: {str(e)}")
            raise

    def get_estatisticas_detalhadas(self, data: datetime) -> Dict:
        """Obtém estatísticas detalhadas para um dia específico"""
        try:
            cursor = self.conn.cursor()
            
            # Estatísticas gerais do dia
            cursor.execute('''
                SELECT tempo_postura_correta,
                       tempo_postura_incorreta,
                       total_analises,
                       media_angulo_ombros,
                       media_angulo_quadril
                FROM estatisticas_diarias
                WHERE data = %s
            ''', (data.date(),))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
            
            # Distribuição por hora
            cursor.execute('''
                SELECT HOUR(data_hora) as hora,
                       COUNT(*) as total,
                       SUM(CASE WHEN postura_correta THEN 1 ELSE 0 END) as corretas
                FROM registros_postura
                WHERE DATE(data_hora) = %s
                GROUP BY HOUR(data_hora)
                ORDER BY hora
            ''', (data.date(),))
            
            distribuicao_hora = cursor.fetchall()
            
            # Análise de tendências
            cursor.execute('''
                SELECT AVG(angulo_ombros) as media_ombros,
                       AVG(angulo_quadril) as media_quadril,
                       COUNT(*) as total
                FROM registros_postura
                WHERE DATE(data_hora) = %s
                AND postura_correta = FALSE
            ''', (data.date(),))
            
            tendencias = cursor.fetchone()
            
            return {
                'estatisticas_gerais': {
                    'tempo_postura_correta': resultado[0],
                    'tempo_postura_incorreta': resultado[1],
                    'total_analises': resultado[2],
                    'media_angulo_ombros': resultado[3],
                    'media_angulo_quadril': resultado[4]
                },
                'distribuicao_hora': [{
                    'hora': row[0],
                    'total': row[1],
                    'corretas': row[2],
                    'percentual': (row[2] / row[1] * 100) if row[1] > 0 else 0
                } for row in distribuicao_hora],
                'tendencias': {
                    'media_angulo_ombros': tendencias[0] if tendencias else 0,
                    'media_angulo_quadril': tendencias[1] if tendencias else 0,
                    'total_incorretas': tendencias[2] if tendencias else 0
                }
            }
        except Exception as e:
            print(f"[ERRO] Falha ao obter estatísticas detalhadas: {str(e)}")
            raise

    def get_historico_postura(self, dias: int = 7) -> List[Dict]:
        """Obtém histórico de postura dos últimos dias"""
        try:
            cursor = self.conn.cursor()
            data_inicio = datetime.now() - timedelta(days=dias)
            
            cursor.execute('''
                SELECT data,
                       tempo_postura_correta,
                       tempo_postura_incorreta,
                       total_analises,
                       media_angulo_ombros,
                       media_angulo_quadril
                FROM estatisticas_diarias
                WHERE data >= %s
                ORDER BY data DESC
            ''', (data_inicio.date(),))
            
            resultados = cursor.fetchall()
            
            return [{
                'data': row[0],
                'tempo_postura_correta': row[1],
                'tempo_postura_incorreta': row[2],
                'total_analises': row[3],
                'media_angulo_ombros': row[4],
                'media_angulo_quadril': row[5]
            } for row in resultados]
        except Exception as e:
            print(f"[ERRO] Falha ao obter histórico: {str(e)}")
            raise

    def exportar_dados_csv(self, caminho: str, dias: int = 7) -> bool:
        """Exporta dados para arquivo CSV"""
        try:
            historico = self.get_historico_postura(dias)
            
            with open(caminho, 'w', newline='') as arquivo:
                writer = csv.DictWriter(arquivo, fieldnames=[
                    'data', 'tempo_postura_correta', 'tempo_postura_incorreta',
                    'total_analises', 'media_angulo_ombros', 'media_angulo_quadril'
                ])
                
                writer.writeheader()
                writer.writerows(historico)
            
            print(f"[INFO] Dados exportados para CSV: {caminho}")
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao exportar CSV: {str(e)}")
            return False

    def exportar_dados_json(self, caminho: str, dias: int = 7) -> bool:
        """Exporta dados para arquivo JSON"""
        try:
            historico = self.get_historico_postura(dias)
            
            with open(caminho, 'w') as arquivo:
                json.dump(historico, arquivo, indent=4, default=str)
            
            print(f"[INFO] Dados exportados para JSON: {caminho}")
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao exportar JSON: {str(e)}")
            return False

    def __del__(self):
        """Fecha a conexão com o banco de dados"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
                print("[INFO] Conexão com banco de dados fechada")
        except Exception as e:
            print(f"[ERRO] Falha ao fechar conexão: {str(e)}") 