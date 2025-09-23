# SnapLinked v3.0 - Dockerfile para Produção
FROM python:3.11-slim

# Metadados
LABEL maintainer="SnapLinked Team <suporte@snaplinked.com>"
LABEL version="3.0.0"
LABEL description="SnapLinked - Automação Profissional LinkedIn"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash snaplinked
USER snaplinked
WORKDIR /home/snaplinked

# Copiar arquivos de dependências
COPY --chown=snaplinked:snaplinked backend/requirements.txt ./

# Instalar dependências Python
RUN pip install --user --no-cache-dir -r requirements.txt

# Instalar navegadores Playwright
RUN python -m playwright install chromium

# Copiar código da aplicação
COPY --chown=snaplinked:snaplinked backend/ ./

# Criar diretórios necessários
RUN mkdir -p instance logs

# Inicializar banco de dados
RUN python init_db.py init

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Comando de inicialização
CMD ["python", "app.py"]
