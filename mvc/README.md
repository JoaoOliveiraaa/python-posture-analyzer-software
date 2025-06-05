# Sistema de Análise de Postura

## 📋 Descrição
Sistema desenvolvido para análise e monitoramento de postura em tempo real utilizando webcam e inteligência artificial. O sistema é capaz de detectar e registrar diferentes tipos de posturas, auxiliando na prevenção de problemas posturais.

## 🚀 Funcionalidades
- Captura de vídeo em tempo real
- Detecção de postura usando MediaPipe
- Registro e histórico de posturas
- Interface gráfica intuitiva
- Exportação de dados em CSV
- Backup automático do banco de dados

## 🛠️ Tecnologias Utilizadas
- Python 3.8+
- OpenCV
- MediaPipe
- SQLite3
- PyQt6
- NumPy

## 📦 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

1. Execute o programa principal:
```bash
python main.py
```

2. Na interface principal:
   - Clique em "Iniciar Câmera" para começar a captura
   - Use "Capturar Postura" para registrar uma postura
   - Acesse "Histórico" para ver registros anteriores
   - Use "Exportar" para salvar dados em CSV

## 📁 Estrutura do Projeto
```
.
├── main.py              # Ponto de entrada do programa
├── requirements.txt     # Dependências do projeto
├── controllers/         # Controladores da aplicação
├── models/             # Modelos e banco de dados
├── views/              # Interface gráfica
└── postura.db          # Banco de dados SQLite
```

## 🔧 Configuração
- Ajuste a resolução da câmera em `config.py`
- Configure o intervalo de backup em `models/database.py`
- Personalize os tipos de postura em `models/postura.py`

## 📊 Banco de Dados
O sistema utiliza SQLite3 com as seguintes tabelas:
- `posturas`: Armazena registros de posturas
- `configuracoes`: Configurações do sistema

## 🔒 Backup
- Backup automático diário
- Localização: `backup/`
- Formato: `postura_YYYYMMDD.db`

## 🤝 Contribuição
1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature
3. Commit suas mudanças
4. Push para a Branch
5. Abra um Pull Request

## 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores
- [Joao Pedro Cunha de Oliveira - RA - 4200984]
- [Luiz Eduardo Marques - RA 4200974]
- [Lucas Frigeri Salaro - RA 4200988]
- [Otávio Rodrigues da Silva - RA 4200992]
