# Estágio 1: Build - instalação de dependências
FROM python:3.11-slim AS builder

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho temporário
WORKDIR /build

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Estágio 2: Runtime - imagem final otimizada
FROM python:3.11-slim AS runtime

# Instalar apenas dependências de runtime necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash --user-group --uid 1000 watchdog

# Diretório de trabalho
WORKDIR /app

# Criar diretório de logs com permissões corretas
RUN mkdir -p /app/logs && chown -R watchdog:watchdog /app

# Script de entrada para corrigir permissões em runtime
COPY --chown=watchdog:watchdog entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar dependências Python do estágio de build
COPY --from=builder /root/.local /home/watchdog/.local

# Copiar arquivos da aplicação
COPY --chown=watchdog:watchdog main.py .
COPY --chown=watchdog:watchdog health_check.py .

# Configurar PATH para incluir binários do usuário
ENV PATH=/home/watchdog/.local/bin:$PATH

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Mudar para usuário não-root
USER watchdog

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python health_check.py || exit 1

# Comando padrão com entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "main.py"]
