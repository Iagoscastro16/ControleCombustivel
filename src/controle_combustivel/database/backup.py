import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from database.connection import DB_PATH,DATA_DIR

BACKUP_DIR = DATA_DIR / "backups"
MAX_BACKUPS = 5


def hash_arquivo(caminho):
    #calcula o hash do arquivo
    with open(caminho,"rb")as f:
        return hashlib.md5(f.read()).hexdigest()
    
def _ultimo_backup():
    if not BACKUP_DIR.exists():
        return None
    backups = sorted(BACKUP_DIR.glob("backup_*.db"))
    return backups[-1] if backups else None
    
def _limpar_backups_antigos():
    backups = sorted(BACKUP_DIR.glob("backup_*.db"))
    while len(backups) > MAX_BACKUPS:
        backups[0].unlink()
        backups.pop(0)


def fazer_backup():
    try:
        if not DB_PATH.exists():
            return False
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        hash_atual = hash_arquivo(DB_PATH)
        ultimo = _ultimo_backup()


        if ultimo and hash_arquivo(ultimo) == hash_atual:
            return False
        
        nome = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.db"
        destino = BACKUP_DIR / nome
        shutil.copy2(DB_PATH,destino)

        _limpar_backups_antigos()


        return True
    
    except Exception as e:
        print(f"Erro ao fazer backup:{e}")
        return False