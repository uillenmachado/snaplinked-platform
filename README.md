# 🚀 SnapLinked v3.0

**Plataforma Profissional de Automação LinkedIn**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)](https://flask.palletsprojects.com)

## 📋 **Sobre o Projeto**

O SnapLinked é uma plataforma completa e profissional para automação de ações no LinkedIn, desenvolvida com tecnologias modernas e foco em segurança, performance e escalabilidade empresarial.

### ✨ **Principais Funcionalidades**

- **Automação Real LinkedIn** com Playwright
- **Autenticação OAuth 2.0** + JWT seguro
- **Dashboard Moderno** e responsivo
- **API RESTful** completa e documentada
- **Persistência de Dados** com SQLAlchemy
- **Monitoramento** e métricas em tempo real
- **Deploy Automatizado** com Docker

### 🎯 **Ações Automatizadas**

- ❤️ **Curtir posts** automaticamente
- 🤝 **Enviar convites** de conexão
- 💬 **Comentar posts** com mensagens personalizadas
- 📊 **Estatísticas detalhadas** de performance
- 🔄 **Histórico completo** de automações

## 🛠️ **Tecnologias Utilizadas**

### **Backend**
- **Python 3.11** - Linguagem principal
- **Flask 3.0** - Framework web moderno
- **SQLAlchemy 2.0** - ORM avançado
- **Playwright 1.48** - Automação web real
- **JWT** - Autenticação segura
- **Structlog** - Logging estruturado

### **Frontend**
- **HTML5/CSS3** - Interface moderna
- **JavaScript ES6+** - Funcionalidades avançadas
- **PWA** - Progressive Web App
- **Service Worker** - Cache inteligente
- **Responsive Design** - Compatibilidade universal

### **Infraestrutura**
- **Docker** - Containerização
- **Nginx** - Proxy reverso e SSL
- **SQLite/PostgreSQL** - Banco de dados
- **OAuth 2.0** - Autenticação LinkedIn

## 🚀 **Instalação Rápida**

### **Pré-requisitos**
- Python 3.8+
- Docker e Docker Compose
- Git

### **1. Clone o Repositório**
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform
```

### **2. Configuração de Ambiente**
```bash
# Copiar arquivo de configuração
cp backend/.env.example backend/.env

# Editar variáveis de ambiente
nano backend/.env
```

### **3. Deploy com Docker (Recomendado)**
```bash
# Deploy de desenvolvimento
./deploy.sh

# Deploy de produção
./deploy.sh
# Escolha opção 2 no menu
```

### **4. Instalação Manual**
```bash
# Criar ambiente virtual
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar navegadores Playwright
playwright install chromium

# Inicializar banco de dados
python init_db.py init

# Executar aplicação
python app.py
```

## 🔧 **Configuração**

### **Variáveis de Ambiente**
```env
# Configurações básicas
SECRET_KEY=sua-chave-secreta-super-segura
FLASK_ENV=production
DEBUG=false

# LinkedIn OAuth (opcional)
LINKEDIN_CLIENT_ID=seu-client-id
LINKEDIN_CLIENT_SECRET=seu-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:5000/auth/linkedin/callback

# Banco de dados
DATABASE_URL=sqlite:///instance/snaplinked.db

# Configurações de automação
DEFAULT_DELAY_MIN=2
DEFAULT_DELAY_MAX=5
MAX_DAILY_ACTIONS=100
```

### **LinkedIn OAuth Setup**
1. Acesse [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Crie uma nova aplicação
3. Configure redirect URI: `http://localhost:5000/auth/linkedin/callback`
4. Copie Client ID e Client Secret para `.env`

## 📖 **Como Usar**

### **1. Acesso à Plataforma**
- Abra `http://localhost:5000` no navegador
- Faça login com LinkedIn OAuth ou login manual
- Acesse o dashboard principal

### **2. Configurar Automações**
- Defina limites diários de ações
- Configure delays entre ações
- Personalize mensagens de comentários

### **3. Executar Automações**
- Selecione o tipo de ação (curtir, conectar, comentar)
- Defina quantidade de ações
- Monitore progresso em tempo real

### **4. Acompanhar Resultados**
- Visualize estatísticas detalhadas
- Analise histórico de automações
- Monitore performance e sucesso

## 📊 **API Endpoints**

### **Autenticação**
```http
POST /api/auth/manual-login    # Login manual
GET  /api/auth/linkedin        # OAuth LinkedIn
POST /api/auth/logout          # Logout
```

### **Automação**
```http
POST /api/automation/like      # Curtir posts
POST /api/automation/connect   # Enviar convites
POST /api/automation/comment   # Comentar posts
GET  /api/automation/sessions  # Histórico de sessões
GET  /api/automation/stats     # Estatísticas
```

### **Sistema**
```http
GET /api/health               # Status da aplicação
GET /api/status               # Status do usuário
```

## 🔒 **Segurança**

### **Recursos Implementados**
- **Autenticação JWT** com refresh tokens
- **Rate limiting** por IP e usuário
- **Input validation** em todas as APIs
- **CSRF protection** automático
- **Security headers** configurados
- **Audit logging** estruturado
- **Criptografia** de dados sensíveis

### **Boas Práticas**
- Use HTTPS em produção
- Configure firewalls adequados
- Monitore logs de segurança
- Mantenha dependências atualizadas
- Use senhas fortes para SECRET_KEY

## 🐳 **Deploy em Produção**

### **Docker Compose**
```bash
# Produção com Nginx e SSL
docker-compose --profile production up -d
```

### **Configurações de Produção**
- Configure certificados SSL válidos
- Use banco PostgreSQL para escala
- Configure backup automático
- Monitore recursos do sistema
- Configure alertas de erro

## 🧪 **Testes**

```bash
# Executar todos os testes
cd backend
python run_tests.py

# Testes com coverage
python run_tests.py --coverage

# Testes específicos
python -m pytest tests/test_api.py
```

## 📈 **Monitoramento**

### **Métricas Disponíveis**
- Performance de automações
- Uso de recursos do sistema
- Estatísticas de usuários
- Logs de erro e debug
- Health checks automáticos

### **Dashboards**
- `/api/health` - Status da aplicação
- `/api/status` - Status do usuário
- Logs estruturados com Structlog

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 **Suporte**

- **Issues**: [GitHub Issues](https://github.com/uillenmachado/snaplinked-platform/issues)
- **Documentação**: [API Documentation](API.md)
- **Instalação**: [Installation Guide](INSTALL.md)
- **Segurança**: [Security Policy](SECURITY.md)

## 🎯 **Roadmap**

### **v3.1 (Próxima)**
- [ ] Integração com mais redes sociais
- [ ] Dashboard analytics avançado
- [ ] API webhooks
- [ ] Automações agendadas

### **v3.2 (Futuro)**
- [ ] Machine Learning para otimização
- [ ] Multi-tenancy
- [ ] Mobile app
- [ ] Integrações CRM

---

**Desenvolvido com ❤️ pela equipe SnapLinked**

[![GitHub](https://img.shields.io/badge/GitHub-uillenmachado-black.svg)](https://github.com/uillenmachado)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/in/uillenmachado)
