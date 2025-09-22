# 🚀 SnapLinked - Versão Real Production-Ready

## 📋 Sobre o Projeto

**SnapLinked** é um sistema completo de automação LinkedIn com funcionalidades reais implementadas. Esta versão inclui OAuth LinkedIn oficial, automação Playwright, comentários com IA Gemini, sistema de filas, WebSocket em tempo real e muito mais.

### ✨ Funcionalidades Reais Implementadas

- 🔐 **OAuth LinkedIn Real** - Autenticação oficial com credenciais configuradas
- 🎭 **Automação Playwright** - Curtidas e comentários reais no LinkedIn
- 🤖 **Gemini AI** - Comentários contextuais gerados por IA
- 📊 **Dashboard Tempo Real** - Interface com WebSocket e métricas ao vivo
- 🔄 **Sistema de Filas** - Jobs com tracking e rate limiting
- 🛡️ **Rate Limiting** - Proteção inteligente contra bloqueios
- 🔒 **Segurança** - Criptografia AES-GCM e JWT tokens
- 📈 **Analytics** - Relatórios e insights detalhados

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **Flask-SocketIO** - WebSocket em tempo real
- **Playwright** - Automação web real
- **Google Generative AI** - Comentários inteligentes
- **SQLAlchemy** - ORM para banco de dados
- **Redis** - Cache e filas de jobs
- **JWT** - Autenticação segura

### Frontend
- **React 18**
- **Vite** - Build tool moderna
- **Tailwind CSS** - Estilização
- **Socket.IO Client** - WebSocket cliente
- **Axios** - Cliente HTTP

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Git
git --version
```

### 2. Clonar Repositório

```bash
git clone <repository-url>
cd snaplinked-real-v1.0
```

### 3. Configurar Backend

```bash
# Navegar para backend
cd snaplinked-backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar browsers Playwright
playwright install
```

### 4. Configurar Variáveis de Ambiente

Criar arquivo `.env` no diretório `snaplinked-backend`:

```env
# LinkedIn OAuth (OBRIGATÓRIO)
LINKEDIN_CLIENT_ID=77jmwin70p0gge
LINKEDIN_CLIENT_SECRET=ZGeGVXoeopPADn4v
LINKEDIN_REDIRECT_URI=http://localhost:3000/auth/linkedin/callback
LINKEDIN_SCOPES=openid profile email

# Gemini AI (OBRIGATÓRIO)
GEMINI_API_KEY=AIzaSyAoCyNdZ7wlwOTFxFGMCCCQrleZ-gmJAJE

# Credenciais LinkedIn para Automação (OBRIGATÓRIO)
LINKEDIN_TEST_EMAIL=metodoivib2b@gmail.com
LINKEDIN_TEST_PASSWORD=Ivib2b2024

# Configurações do Sistema
SECRET_KEY=snaplinked-secret-key-2024
DATABASE_URL=sqlite:///snaplinked.db
REDIS_URL=redis://localhost:6379/0

# Configurações de Rate Limiting
RATE_LIMIT_LIKES_PER_HOUR=50
RATE_LIMIT_COMMENTS_PER_HOUR=20
RATE_LIMIT_CONNECTIONS_PER_DAY=100

# Configurações de Segurança
ENCRYPTION_KEY=sua-chave-de-criptografia-32-chars
JWT_SECRET_KEY=sua-jwt-secret-key
```

### 5. Configurar Frontend

```bash
# Navegar para frontend
cd ../snaplinked-frontend

# Instalar dependências
npm install --legacy-peer-deps

# Criar arquivo .env
echo "VITE_API_URL=http://localhost:5000" > .env
echo "VITE_WEBSOCKET_URL=http://localhost:5000" >> .env
echo "VITE_APP_VERSION=5.0.0-real" >> .env
```

## 🏃‍♂️ Executar o Sistema

### Desenvolvimento

**Terminal 1 - Backend:**
```bash
cd snaplinked-backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd snaplinked-frontend
npm run dev
```

### Produção

**Docker Compose:**
```bash
docker-compose up -d
```

**Manual:**
```bash
# Backend
cd snaplinked-backend
gunicorn -w 4 -b 0.0.0.0:5000 main:app

# Frontend (build)
cd snaplinked-frontend
npm run build
# Servir com nginx ou servidor web
```

## 🔧 Uso do Sistema

### 1. Acessar Dashboard

Abrir navegador em: `http://localhost:3000`

### 2. Autenticação LinkedIn

- **OAuth:** Clique em "Conectar com LinkedIn OAuth"
- **Manual:** Use credenciais `metodoivib2b@gmail.com` / `Ivib2b2024`

### 3. Executar Automações

- **Curtir Posts:** Clique em "Curtir Post"
- **Comentários IA:** Clique em "Comentário IA"
- **Conexões:** Clique em "Enviar Conexão"

### 4. Monitorar Jobs

- **Ver Jobs:** Clique em "Ver Jobs"
- **Estatísticas:** Clique em "Estatísticas"
- **Tempo Real:** Observe o log de atividades

## 📡 API Endpoints

### Autenticação
- `POST /api/auth/login` - Login de usuário
- `GET /auth/linkedin/start` - Iniciar OAuth LinkedIn
- `GET /auth/linkedin/callback` - Callback OAuth

### Automação
- `POST /api/automation/login` - Login Playwright
- `POST /api/automation/like` - Curtir post
- `POST /api/automation/comment` - Comentar post
- `GET /api/automation/status` - Status automação

### IA
- `POST /api/ai/generate-comment` - Gerar comentário IA
- `GET /api/ai/test` - Testar conexão Gemini

### Jobs
- `GET /api/jobs` - Listar jobs
- `GET /api/jobs/<id>` - Obter job específico
- `GET /api/jobs/stats` - Estatísticas jobs

### Sistema
- `GET /api/health` - Health check
- `GET /api/stats/dashboard` - Estatísticas dashboard

## 🧪 Testes

### Testes Automatizados
```bash
cd snaplinked-backend
pytest tests/
```

### Testes Manuais
1. Abrir `http://localhost:5000`
2. Testar cada funcionalidade no dashboard
3. Verificar logs em tempo real
4. Confirmar automações no LinkedIn

### Testes de Integração
```bash
# Testar OAuth LinkedIn
curl -X GET http://localhost:5000/auth/linkedin/start

# Testar Gemini AI
curl -X GET http://localhost:5000/api/ai/test

# Testar Health Check
curl -X GET http://localhost:5000/api/health
```

## 📊 Monitoramento

### Logs
- **Backend:** Console do Python
- **Frontend:** Console do navegador
- **WebSocket:** Log de atividades em tempo real

### Métricas
- **Jobs:** Pendentes, executando, concluídos, falhados
- **Rate Limiting:** Ações restantes por período
- **Sistema:** Status operacional, conexões ativas

### Health Check
```bash
curl http://localhost:5000/api/health
```

## 🔒 Segurança

### Credenciais
- **OAuth LinkedIn:** Configurado com credenciais reais
- **Gemini AI:** API key configurada
- **Criptografia:** AES-GCM para dados sensíveis
- **JWT:** Tokens seguros para autenticação

### Rate Limiting
- **Curtidas:** 50 por hora
- **Comentários:** 20 por hora
- **Conexões:** 100 por dia
- **Ações:** 5 por minuto

### Proteções
- **CORS:** Configurado adequadamente
- **Headers:** Segurança HTTP
- **Validação:** Entrada de dados
- **Logs:** Auditoria completa

## 🚀 Deploy em Produção

### Heroku
```bash
# Configurar Heroku
heroku create snaplinked-app
heroku config:set LINKEDIN_CLIENT_ID=77jmwin70p0gge
heroku config:set GEMINI_API_KEY=AIzaSyAoCyNdZ7wlwOTFxFGMCCCQrleZ-gmJAJE
# ... outras variáveis

# Deploy
git push heroku main
```

### AWS/DigitalOcean
```bash
# Usar Docker
docker build -t snaplinked .
docker run -p 5000:5000 snaplinked
```

### VPS Manual
```bash
# Instalar dependências
sudo apt update
sudo apt install python3 python3-pip nodejs npm nginx

# Configurar aplicação
# ... seguir passos de instalação

# Configurar nginx
sudo cp nginx.conf /etc/nginx/sites-available/snaplinked
sudo ln -s /etc/nginx/sites-available/snaplinked /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Configurar systemd
sudo cp snaplinked.service /etc/systemd/system/
sudo systemctl enable snaplinked
sudo systemctl start snaplinked
```

## 📞 Suporte

### Documentação
- **API:** `/docs` endpoint
- **Frontend:** Comentários no código
- **Arquitetura:** Diagramas em `/docs`

### Troubleshooting
- **Logs:** Verificar console e arquivos de log
- **Health:** Acessar `/api/health`
- **Status:** Monitorar dashboard

### Contato
- **Email:** suporte@snaplinked.com
- **GitHub:** Issues no repositório
- **Discord:** Servidor da comunidade

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📈 Roadmap

### Versão 5.1
- [ ] Suporte a múltiplas contas LinkedIn
- [ ] Agendamento de automações
- [ ] Relatórios avançados
- [ ] Integração com CRM

### Versão 5.2
- [ ] Mobile app
- [ ] API pública
- [ ] Webhooks
- [ ] Integrações terceiros

---

**SnapLinked v5.0.0-real** - Sistema completo de automação LinkedIn com funcionalidades reais implementadas.

*Desenvolvido com ❤️ para automação profissional do LinkedIn.*
