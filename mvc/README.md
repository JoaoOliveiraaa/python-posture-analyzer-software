# Sistema de Análise de Postura

Sistema desenvolvido para monitorar e analisar a postura do usuário em tempo real, utilizando visão computacional e machine learning.

## Funcionalidades

- Captura de vídeo em tempo real via webcam
- Detecção de postura usando MediaPipe Pose
- Análise de ângulos dos ombros e quadril
- Alertas visuais e sonoros para postura incorreta
- Sugestões de correção de postura
- Estatísticas detalhadas de uso
- Exportação de dados em CSV e JSON
- Interface gráfica moderna e intuitiva

## Requisitos

- Python 3.8 ou superior
- Webcam
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/analise-postura.git
cd analise-postura
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o programa principal:
```bash
python main.py
```

2. Na interface gráfica:
   - Clique em "Iniciar Monitoramento" para começar
   - Ajuste as configurações da câmera conforme necessário
   - Monitore sua postura em tempo real
   - Consulte as estatísticas e exporte os dados quando desejar

## Estrutura do Projeto

```
.
├── controllers/
│   └── controller.py    # Lógica de controle e processamento
├── models/
│   └── model.py        # Gerenciamento de dados e banco de dados
├── views/
│   └── view.py         # Interface gráfica
├── main.py             # Ponto de entrada do programa
├── requirements.txt    # Dependências do projeto
└── README.md          # Documentação
```

## Banco de Dados

O sistema utiliza SQLite para armazenar:
- Registros de análise de postura
- Estatísticas diárias
- Histórico de uso

## Logs

O sistema mantém logs detalhados de:
- Operações do banco de dados
- Erros e exceções
- Eventos importantes
- Estatísticas de uso

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Seu Nome - seu.email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/analise-postura](https://github.com/seu-usuario/analise-postura) 