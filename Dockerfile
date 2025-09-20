# SnapLinked - Dockerfile para Produção
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chromium para Playwright
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY snaplinked-backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiar código da aplicação
COPY snaplinked-backend/ .

# Criar diretório para banco de dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Configurar variáveis de ambiente
ENV FLASK_ENV=production
ENV PORT=5000
ENV PYTHONPATH=/app

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
