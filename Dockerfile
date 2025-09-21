FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
