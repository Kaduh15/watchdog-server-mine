#!/usr/bin/env python3
"""
Health check script para o watchdog container.
Verifica se o processo principal está funcionando corretamente.
"""

import os
import sys
import psutil
from datetime import datetime, timedelta

def check_health():
    """
    Verifica a saúde do container watchdog.
    Retorna 0 se saudável, 1 se não saudável.
    """
    try:
        # Verificar se o processo principal está rodando
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'main.py' in ' '.join(proc.info['cmdline'] or []):
                    # Processo encontrado e rodando
                    
                    # Verificar se o arquivo de log foi atualizado recentemente (últimos 10 minutos)
                    log_file = '/app/logs/watchdog.log'
                    if os.path.exists(log_file):
                        log_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                        if datetime.now() - log_mtime > timedelta(minutes=10):
                            print("UNHEALTHY: Log file não atualizado há mais de 10 minutos")
                            return 1
                    
                    print("HEALTHY: Watchdog está rodando normalmente")
                    return 0
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print("UNHEALTHY: Processo main.py não encontrado")
        return 1
        
    except Exception as e:
        print(f"UNHEALTHY: Erro durante health check: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())