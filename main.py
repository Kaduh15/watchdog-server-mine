import time
import os
from mcstatus import JavaServer
import mcrcon
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT", 25565))
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))       # Intervalo quando online
OFFLINE_INTERVAL = int(os.getenv("OFFLINE_INTERVAL", 7200)) # Intervalo quando offline (2h padrão)
EMPTY_THRESHOLD = int(os.getenv("EMPTY_THRESHOLD", 5))

def main():
    empty_count = 0

    while True:
        try:
            server = JavaServer.lookup(f"{SERVER_HOST}:{SERVER_PORT}")
            status = server.status()
            players_online = status.players.online
            print(f"{players_online} players online")

            if players_online == 0:
                empty_count += 1
            else:
                empty_count = 0

            if empty_count >= EMPTY_THRESHOLD:
                print("Sem players por muito tempo. Enviando comando de stop...")
                try:
                    with mcrcon.MCRcon(SERVER_HOST, RCON_PASSWORD, port=RCON_PORT) as rcon:
                        rcon.command("stop")
                except Exception as e:
                    print(f"Falha ao enviar comando RCON: {e}")

                empty_count = 0

            # Espera normal (servidor online)
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            # Se não conseguir se conectar, assume que o servidor está OFF
            print(f"Servidor offline ou inacessível: {e}")
            print(f"Aguardando {OFFLINE_INTERVAL} segundos antes da próxima tentativa...")
            time.sleep(OFFLINE_INTERVAL)

if __name__ == "__main__":
    main()

