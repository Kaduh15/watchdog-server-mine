#!/usr/bin/env python3
"""
Health check script para o watchdog container.
Verifica se o processo principal está funcionando corretamente.
"""

import os
import sys
from datetime import datetime, timedelta

def check_health():
    """
    Verifica a saúde do container watchdog.
    Retorna 0 se saudável, 1 se não saudável.
    """
    try:
        # Método mais simples: verificar se existe processo Python rodando
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'main.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Processo encontrado, verificar log se existir
            log_file = '/app/logs/watchdog.log'
            if os.path.exists(log_file):
                # Verificar se foi atualizado nos últimos 15 minutos
                log_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                if datetime.now() - log_mtime > timedelta(minutes=15):
                    print("UNHEALTHY: Log file não atualizado há mais de 15 minutos")
                    return 1
            
            print("HEALTHY: Watchdog está rodando normalmente")
            return 0
        else:
            print("UNHEALTHY: Processo main.py não encontrado")
            return 1
        
    except Exception as e:
        print(f"UNHEALTHY: Erro durante health check: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())