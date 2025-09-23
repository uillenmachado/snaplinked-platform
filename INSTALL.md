# 🚀 SnapLinked v3.0 - Guia de Instalação para Produção

Este guia fornece instruções detalhadas para instalar e configurar o SnapLinked v3.0 em ambiente de produção.

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux**: Ubuntu 20.04+ (recomendado), CentOS 8+, Debian 11+
- **Windows**: Windows Server 2019+ com WSL2
- **macOS**: macOS 11+ (para desenvolvimento)

### Software Necessário
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.25+
- **Certificados SSL**: Para HTTPS em produção

### Hardware Mínimo
- **CPU**: 2 cores
- **RAM**: 4GB
- **Armazenamento**: 20GB livres
- **Rede**: Conexão estável com internet

## 🔧 Instalação Rápida

### 1. Clonar o Repositório
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform
```

### 2. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp backend/.env.example backend/.env

# Editar configurações
nano backend/.env
```

**Configurações obrigatórias:**
```env
# Segurança (OBRIGATÓRIO)
SECRET_KEY=sua-chave-super-secreta-de-32-caracteres-ou-mais

# Ambiente
FLASK_ENV=production
FLASK_DEBUG=false
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Banco de dados
DATABASE_URL=sqlite:///instance/snaplinked.db

# LinkedIn OAuth (opcional mas recomendado)
LINKEDIN_CLIENT_ID=seu-client-id-linkedin
LINKEDIN_CLIENT_SECRET=seu-client-secret-linkedin
LINKEDIN_REDIRECT_URI=https://seudominio.com/auth/linkedin/callback

# Configurações de automação
AUTOMATION_DELAY=2
MAX_ACTIONS_PER_SESSION=50
```

### 3. Deploy Automatizado
```bash
# Tornar script executável
chmod +x deploy.sh

# Executar deploy
./deploy.sh
```

Escolha a opção **2** para deploy de produção com HTTPS.

## 🔐 Configuração de Segurança

### Certificados SSL

#### Opção 1: Let's Encrypt (Recomendado)
```bash
# Instalar Certbot
sudo apt update
sudo apt install certbot

# Obter certificado
sudo certbot certonly --standalone -d seudominio.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/seudominio.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/seudominio.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*.pem
```

#### Opção 2: Certificado Próprio
```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

### Firewall
```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

## 🌐 Configuração de Domínio

### DNS
Configure os registros DNS para apontar para seu servidor:
```
A    seudominio.com    IP_DO_SERVIDOR
AAAA seudominio.com    IPv6_DO_SERVIDOR (opcional)
```

### Nginx (Incluído no Docker Compose)
O Nginx está pré-configurado com:
- Redirecionamento HTTP → HTTPS
- Rate limiting
- Headers de segurança
- Compressão Gzip
- Cache de arquivos estáticos

## 📊 Monitoramento

### Logs
```bash
# Logs da aplicação
docker-compose logs -f snaplinked

# Logs do Nginx
docker-compose logs -f nginx

# Logs do sistema
sudo journalctl -u docker -f
```

### Health Check
```bash
# Verificar saúde da aplicação
curl https://seudominio.com/api/health

# Resposta esperada:
{
  "status": "ok",
  "version": "3.0.0",
  "timestamp": "2025-09-23T21:30:00Z"
}
```

### Métricas
```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats

# Espaço em disco
df -h
```

## 🔄 Backup e Restauração

### Backup Automático
```bash
# Criar backup manual
./deploy.sh
# Escolher opção 5

# Backup automático via cron
echo "0 2 * * * cd /caminho/para/snaplinked && ./deploy.sh <<< '5'" | crontab -
```

### Restauração
```bash
# Parar aplicação
docker-compose down

# Restaurar banco
cp backups/backup_snaplinked_YYYYMMDD_HHMMSS.db backend/instance/snaplinked.db

# Reiniciar aplicação
docker-compose up -d
```

## 🚀 Otimizações de Performance

### 1. Configuração do Sistema
```bash
# Aumentar limites de arquivo
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Otimizar kernel para rede
echo "net.core.somaxconn = 65536" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65536" >> /etc/sysctl.conf
sysctl -p
```

### 2. Docker Otimizado
```bash
# Configurar Docker daemon
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
EOF

sudo systemctl restart docker
```

### 3. Banco de Dados
Para alta performance, considere migrar para PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/snaplinked
```

## 🔧 Manutenção

### Atualizações
```bash
# Atualizar código
git pull origin main

# Rebuild e restart
docker-compose up --build -d

# Verificar saúde
curl https://seudominio.com/api/health
```

### Limpeza
```bash
# Limpar imagens antigas
docker image prune -f

# Limpar volumes não utilizados
docker volume prune -f

# Limpar logs antigos
sudo find /var/lib/docker/containers -name "*.log" -exec truncate -s 0 {} \;
```

## 🆘 Solução de Problemas

### Problemas Comuns

#### 1. Aplicação não inicia
```bash
# Verificar logs
docker-compose logs snaplinked

# Verificar configurações
cat backend/.env

# Testar conectividade
docker-compose exec snaplinked python -c "import requests; print(requests.get('http://localhost:5000/api/health').json())"
```

#### 2. Erro de SSL
```bash
# Verificar certificados
openssl x509 -in ssl/cert.pem -text -noout

# Testar SSL
openssl s_client -connect localhost:443 -servername seudominio.com
```

#### 3. Performance lenta
```bash
# Verificar recursos
docker stats

# Verificar logs de erro
docker-compose logs snaplinked | grep ERROR

# Verificar conectividade com LinkedIn
docker-compose exec snaplinked curl -I https://linkedin.com
```

### Logs de Debug
```bash
# Habilitar debug temporariamente
docker-compose exec snaplinked bash -c "
export FLASK_DEBUG=true
python app.py
"
```

## 📞 Suporte

### Documentação
- **README**: Documentação principal
- **CHANGELOG**: Histórico de mudanças
- **API Docs**: Endpoints disponíveis

### Contato
- **Email**: suporte@snaplinked.com
- **GitHub Issues**: https://github.com/uillenmachado/snaplinked-platform/issues
- **Documentação**: https://snaplinked.com/docs

### Suporte Comercial
Para suporte empresarial, customizações ou consultoria:
- **Email**: comercial@snaplinked.com
- **Website**: https://snaplinked.com/enterprise

---

**SnapLinked v3.0** - Automação LinkedIn de nível empresarial 🚀
