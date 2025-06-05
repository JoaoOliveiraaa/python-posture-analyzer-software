import os
import shutil
from datetime import datetime
import zipfile

def criar_backup():
    # Criar diretório de backup se não existir
    if not os.path.exists('backup'):
        os.makedirs('backup')
    
    # Nome do arquivo de backup com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_nome = f'backup/postura_backup_{timestamp}'
    
    # Lista de arquivos e diretórios para backup
    arquivos_backup = [
        'main.py',
        'requirements.txt',
        'README.md',
        'MANUAL.md',
        'APRESENTACAO.md',
        'LICENSE',
        'postura.db',
        'controllers',
        'models',
        'views'
    ]
    
    # Criar arquivo ZIP
    with zipfile.ZipFile(f'{backup_nome}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in arquivos_backup:
            if os.path.exists(arquivo):
                if os.path.isdir(arquivo):
                    for root, dirs, files in os.walk(arquivo):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, '.')
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(arquivo)
    
    print(f'Backup criado com sucesso: {backup_nome}.zip')
    
    # Manter apenas os 5 backups mais recentes
    backups = sorted([f for f in os.listdir('backup') if f.endswith('.zip')])
    if len(backups) > 5:
        for backup_antigo in backups[:-5]:
            os.remove(os.path.join('backup', backup_antigo))
            print(f'Backup antigo removido: {backup_antigo}')

if __name__ == '__main__':
    criar_backup() 