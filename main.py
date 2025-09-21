import time
import os
import sys
import signal
import logging
from datetime import datetime
from mcstatus import JavaServer
import mcrcon
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/app/logs/watchdog.log', mode='a') if os.path.exists('/app/logs') else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Variável global para controle de shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    logger.info(f"Recebido sinal {signum}. Iniciando shutdown gracioso...")
    shutdown_requested = True

# Registrar handlers de sinal
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Carregar variáveis do .env
load_dotenv()

# Validar variáveis obrigatórias
SERVER_HOST = os.getenv("SERVER_HOST")
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

if not SERVER_HOST:
    logger.error("SERVER_HOST é obrigatório. Configure no arquivo .env")
    sys.exit(1)

if not RCON_PASSWORD:
    logger.error("RCON_PASSWORD é obrigatório. Configure no arquivo .env")
    sys.exit(1)

SERVER_PORT = int(os.getenv("SERVER_PORT", 25565))
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))       # Intervalo quando online
OFFLINE_INTERVAL = int(os.getenv("OFFLINE_INTERVAL", 7200)) # Intervalo quando offline (2h padrão)
EMPTY_THRESHOLD = int(os.getenv("EMPTY_THRESHOLD", 5))

logger.info(f"Watchdog iniciado - Servidor: {SERVER_HOST}:{SERVER_PORT}")
logger.info(f"Configurações - Check: {CHECK_INTERVAL}s, Offline: {OFFLINE_INTERVAL}s, Threshold: {EMPTY_THRESHOLD}")

def main():
    empty_count = 0
    
    while not shutdown_requested:
        try:
            server = JavaServer.lookup(f"{SERVER_HOST}:{SERVER_PORT}")
            status = server.status()
            players_online = status.players.online
            logger.info(f"{players_online} players online")

            if players_online == 0:
                empty_count += 1
                logger.debug(f"Contador vazio: {empty_count}/{EMPTY_THRESHOLD}")
            else:
                empty_count = 0

            if empty_count >= EMPTY_THRESHOLD:
                logger.warning(f"Sem players por {empty_count} verificações. Enviando comando de stop...")
                try:
                    with mcrcon.MCRcon(SERVER_HOST, RCON_PASSWORD, port=RCON_PORT) as rcon:
                        rcon.command("stop")
                    logger.info("Comando stop enviado com sucesso")
                except Exception as e:
                    logger.error(f"Falha ao enviar comando RCON: {e}")

                empty_count = 0

            # Espera normal (servidor online) com verificação de shutdown
            for _ in range(CHECK_INTERVAL):
                if shutdown_requested:
                    break
                time.sleep(1)

        except Exception as e:
            # Se não conseguir se conectar, assume que o servidor está OFF
            logger.warning(f"Servidor offline ou inacessível: {e}")
            logger.info(f"Aguardando {OFFLINE_INTERVAL} segundos antes da próxima tentativa...")
            
            # Espera com verificação de shutdown
            for _ in range(OFFLINE_INTERVAL):
                if shutdown_requested:
                    break
                time.sleep(1)
    
    logger.info("Watchdog finalizado graciosamente")

if __name__ == "__main__":
    main()

