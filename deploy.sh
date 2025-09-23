#!/bin/bash
# SnapLinked v3.0 - Script de Deploy Automatizado

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    SnapLinked v3.0                          ║"
echo "║              Script de Deploy Automatizado                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se está no diretório correto
if [ ! -f "README.md" ] || [ ! -d "backend" ]; then
    log_error "Execute este script no diretório raiz do projeto SnapLinked"
    exit 1
fi

# Verificar dependências
log_info "Verificando dependências..."

if ! command -v docker &> /dev/null; then
    log_error "Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

log_success "Dependências verificadas"

# Opções de deploy
echo ""
echo "Escolha o tipo de deploy:"
echo "1) Desenvolvimento (HTTP, porta 5000)"
echo "2) Produção (HTTPS, porta 80/443)"
echo "3) Apenas build da imagem"
echo "4) Executar testes"
echo "5) Backup do banco de dados"

read -p "Digite sua escolha (1-5): " choice

case $choice in
    1)
        log_info "Iniciando deploy de desenvolvimento..."
        
        # Parar containers existentes
        docker-compose down 2>/dev/null || true
        
        # Build e start
        docker-compose up --build -d snaplinked
        
        log_success "Deploy de desenvolvimento concluído!"
        log_info "Aplicação disponível em: http://localhost:5000"
        log_info "API Health: http://localhost:5000/api/health"
        ;;
        
    2)
        log_info "Iniciando deploy de produção..."
        
        # Verificar certificados SSL
        if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
            log_warning "Certificados SSL não encontrados em ./ssl/"
            log_info "Criando certificados auto-assinados para teste..."
            
            mkdir -p ssl
            openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
                -subj "/C=BR/ST=SP/L=São Paulo/O=SnapLinked/CN=localhost"
            
            log_warning "ATENÇÃO: Use certificados válidos em produção real!"
        fi
        
        # Deploy com Nginx
        docker-compose --profile production up --build -d
        
        log_success "Deploy de produção concluído!"
        log_info "Aplicação disponível em: https://localhost"
        log_info "HTTP redireciona automaticamente para HTTPS"
        ;;
        
    3)
        log_info "Fazendo build da imagem Docker..."
        
        docker build -t snaplinked:3.0.0 .
        docker tag snaplinked:3.0.0 snaplinked:latest
        
        log_success "Build concluído!"
        log_info "Imagens criadas: snaplinked:3.0.0 e snaplinked:latest"
        ;;
        
    4)
        log_info "Executando testes..."
        
        cd backend
        
        # Verificar se venv existe
        if [ ! -d "venv" ]; then
            log_info "Criando ambiente virtual..."
            python3 -m venv venv
        fi
        
        # Ativar venv e instalar dependências
        source venv/bin/activate
        pip install -r requirements.txt > /dev/null 2>&1
        
        # Executar testes
        python run_tests.py
        
        deactivate
        cd ..
        
        log_success "Testes concluídos!"
        ;;
        
    5)
        log_info "Fazendo backup do banco de dados..."
        
        timestamp=$(date +"%Y%m%d_%H%M%S")
        backup_file="backup_snaplinked_${timestamp}.db"
        
        if [ -f "backend/instance/snaplinked.db" ]; then
            cp backend/instance/snaplinked.db "backups/${backup_file}"
            mkdir -p backups
            log_success "Backup criado: backups/${backup_file}"
        else
            log_warning "Banco de dados não encontrado"
        fi
        ;;
        
    *)
        log_error "Opção inválida"
        exit 1
        ;;
esac

# Mostrar status dos containers
echo ""
log_info "Status dos containers:"
docker-compose ps

# Mostrar logs recentes
echo ""
log_info "Logs recentes (últimas 10 linhas):"
docker-compose logs --tail=10 snaplinked

echo ""
log_success "Deploy finalizado com sucesso!"
echo ""
echo "Comandos úteis:"
echo "  docker-compose logs -f snaplinked    # Ver logs em tempo real"
echo "  docker-compose restart snaplinked    # Reiniciar aplicação"
echo "  docker-compose down                  # Parar todos os serviços"
echo "  docker-compose exec snaplinked bash  # Acessar container"
echo ""
