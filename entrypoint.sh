#!/bin/bash
set -e

# Corrigir permissões do diretório de logs se existir
if [ -d "/app/logs" ]; then
    # Tentar corrigir permissões (pode falhar se não for root no host)
    touch /app/logs/watchdog.log 2>/dev/null || true
    chmod 666 /app/logs/watchdog.log 2>/dev/null || true
fi

# Executar o comando principal
exec "$@"