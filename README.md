# 🐕 Minecraft Server Watchdog

Um sistema inteligente de monitoramento para servidores Minecraft que automaticamente gerencia o servidor baseado na atividade dos jogadores.

## 📋 Funcionalidades

- ✅ **Monitoramento Contínuo**: Verifica o status do servidor e número de jogadores online
- ✅ **Desligamento Automático**: Para o servidor quando não há jogadores por um período configurável
- ✅ **Intervalos Inteligentes**: Diferentes intervalos para servidor online/offline para otimizar recursos
- ✅ **Controle via RCON**: Usa RCON para enviar comandos ao servidor Minecraft
- ✅ **Containerizado**: Suporte completo ao Docker com Docker Compose
- ✅ **Configuração Flexível**: Todas as configurações via variáveis de ambiente

## 🚀 Como Funciona

1. **Servidor Online**: Monitora a cada `CHECK_INTERVAL` segundos (padrão: 60s)
2. **Jogadores Online**: Reseta contador de verificações vazias
3. **Servidor Vazio**: Incrementa contador quando 0 jogadores online
4. **Threshold Atingido**: Após `EMPTY_THRESHOLD` verificações vazias consecutivas, envia comando `stop` via RCON
5. **Servidor Offline**: Aguarda `OFFLINE_INTERVAL` segundos (padrão: 2h) antes da próxima tentativa

## 📦 Instalação

### Opção 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Kaduh15/watchdog-server-mine.git
cd watchdog-server-mine

# Configure as variáveis de ambiente
cp .env.exemplo .env
# Edite o arquivo .env com suas configurações

# Execute com Docker Compose
docker-compose up -d
```

### Opção 2: Python Local

```bash
# Clone o repositório
git clone https://github.com/Kaduh15/watchdog-server-mine.git
cd watchdog-server-mine

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.exemplo .env
# Edite o arquivo .env com suas configurações

# Execute o watchdog
python main.py
```

## ⚙️ Configuração

### Variáveis de Ambiente

Copie o arquivo `.env.exemplo` para `.env` e configure as seguintes variáveis:

```bash
# Configurações do servidor Minecraft
SERVER_HOST=seu-servidor-minecraft.com
SERVER_PORT=25565
RCON_PORT=25575
RCON_PASSWORD=sua-senha-rcon-aqui

# Configurações do watchdog
# CHECK_INTERVAL: Intervalo entre verificações quando servidor está online (segundos)
CHECK_INTERVAL=60
# OFFLINE_INTERVAL: Intervalo entre verificações quando servidor está offline (segundos - 7200 = 2 horas)
OFFLINE_INTERVAL=7200
# EMPTY_THRESHOLD: Quantas verificações vazias antes de enviar comando stop
EMPTY_THRESHOLD=5
```

### Explicação das Configurações

| Variável | Descrição | Valor Padrão | Exemplo |
|----------|-----------|--------------|---------|
| `SERVER_HOST` | IP ou domínio do servidor Minecraft | - | `minecraft.exemplo.com` |
| `SERVER_PORT` | Porta do servidor Minecraft | `25565` | `25565` |
| `RCON_PORT` | Porta RCON do servidor | `25575` | `25575` |
| `RCON_PASSWORD` | Senha RCON configurada no servidor | - | `minhasenha123` |
| `CHECK_INTERVAL` | Intervalo de verificação quando online (segundos) | `60` | `30` (30s) |
| `OFFLINE_INTERVAL` | Intervalo quando servidor offline (segundos) | `7200` | `3600` (1h) |
| `EMPTY_THRESHOLD` | Verificações vazias antes de parar servidor | `5` | `10` |

### Configuração do Servidor Minecraft

Para que o watchdog funcione, você precisa habilitar RCON no seu servidor Minecraft:

**server.properties:**
```properties
enable-rcon=true
rcon.port=25575
rcon.password=sua-senha-rcon-aqui
```

## 📊 Exemplos de Uso

### Cenário 1: Servidor de Desenvolvimento
```bash
CHECK_INTERVAL=30      # Verifica a cada 30 segundos
EMPTY_THRESHOLD=3      # Para após 3 verificações vazias (1.5 minutos)
OFFLINE_INTERVAL=1800  # Aguarda 30 minutos quando offline
```

### Cenário 2: Servidor de Produção
```bash
CHECK_INTERVAL=120     # Verifica a cada 2 minutos  
EMPTY_THRESHOLD=10     # Para após 10 verificações vazias (20 minutos)
OFFLINE_INTERVAL=7200  # Aguarda 2 horas quando offline
```

### Cenário 3: Servidor Econômico
```bash
CHECK_INTERVAL=60      # Verifica a cada 1 minuto
EMPTY_THRESHOLD=5      # Para após 5 verificações vazias (5 minutos)
OFFLINE_INTERVAL=14400 # Aguarda 4 horas quando offline
```

## 🐳 Docker

### Docker Compose

O projeto inclui um `docker-compose.yml` configurado:

```yaml
version: '3.8'

services:
  watchdog:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: minecraft-watchdog
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Comandos Docker Úteis

```bash
# Iniciar o watchdog
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar o watchdog
docker-compose down

# Reconstruir após mudanças no código
docker-compose up -d --build
```

## 📝 Logs

O watchdog gera logs detalhados sobre suas operações:

```
5 players online
3 players online
1 players online
0 players online
0 players online
0 players online
0 players online
0 players online
Sem players por muito tempo. Enviando comando de stop...
Servidor offline ou inacessível: [Errno 111] Connection refused
Aguardando 7200 segundos antes da próxima tentativa...
```

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
watchdog-server-mine/
├── main.py              # Script principal do watchdog
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Orquestração Docker
├── .env.exemplo        # Template de configuração
├── .gitignore          # Arquivos ignorados pelo Git
├── .dockerignore       # Arquivos ignorados pelo Docker
└── README.md           # Documentação
```

### Dependências

- **mcstatus**: Para consultar status do servidor Minecraft
- **mcrcon**: Para enviar comandos RCON
- **python-dotenv**: Para carregar variáveis de ambiente

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🆘 Solução de Problemas

### Erro de Conexão RCON
```
Falha ao enviar comando RCON: [Errno 111] Connection refused
```
**Solução**: Verifique se RCON está habilitado no servidor e a senha está correta.

### Servidor não para
```
0 players online (repetindo)
```
**Solução**: Verifique se `EMPTY_THRESHOLD` está configurado corretamente e se o RCON está funcionando.

### Docker não inicia
```
ERROR: Couldn't connect to Docker daemon
```
**Solução**: Certifique-se que o Docker está instalado e rodando.

## 📞 Suporte

- 🐛 [Reportar Bug](https://github.com/Kaduh15/watchdog-server-mine/issues)
- 💡 [Solicitar Feature](https://github.com/Kaduh15/watchdog-server-mine/issues)
- 📖 [Documentação](https://github.com/Kaduh15/watchdog-server-mine/wiki)

---

⭐ **Se este projeto foi útil, dê uma estrela no GitHub!** ⭐