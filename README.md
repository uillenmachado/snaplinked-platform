# SnapLinked - LinkedIn Automation Platform

![SnapLinked Logo](https://img.shields.io/badge/SnapLinked-LinkedIn%20Automation-blue?style=for-the-badge&logo=linkedin)

**SnapLinked** é uma plataforma SaaS completa para automação de networking no LinkedIn, desenvolvida com tecnologias modernas e foco em experiência do usuário e performance.

## 🚀 **Demonstração**

🌐 **[Acesse a Aplicação](https://kkh7ikc7v7gg.manus.space)**

## ✨ **Funcionalidades Principais**

### 🤖 **Automações Inteligentes**
- **Solicitações de Conexão** automatizadas com personalização
- **Mensagens de Follow-up** com templates dinâmicos
- **Visualizações de Perfil** estratégicas
- **Agendamento Inteligente** com horários otimizados
- **Limites Seguros** para evitar restrições do LinkedIn

### 📊 **Analytics Avançados**
- **Dashboard em Tempo Real** com métricas detalhadas
- **Gráficos Interativos** de performance
- **Insights Automatizados** e recomendações
- **Relatórios Exportáveis** em múltiplos formatos
- **Análise de Palavras-chave** mais eficazes

### 👥 **Gerenciamento de Contas**
- **Múltiplas Contas LinkedIn** em uma interface
- **Verificação Automática** de status das contas
- **Monitoramento de Limites** diários
- **Rotação Inteligente** entre contas

### ⚙️ **Configurações Avançadas**
- **Perfil Personalizado** com informações completas
- **Notificações Configuráveis** (email e push)
- **Segurança Robusta** com 2FA
- **Automação Customizável** com delays e horários

## 🛠️ **Tecnologias Utilizadas**

### **Frontend**
- **React 18** com Hooks e Context API
- **Vite** para build otimizado
- **Tailwind CSS** para estilização
- **Shadcn/ui** para componentes
- **Lucide React** para ícones
- **React Router** para navegação

### **Backend**
- **Flask** (Python) para API REST
- **SQLAlchemy** para ORM
- **JWT** para autenticação
- **Celery** para tarefas assíncronas
- **Playwright** para automação web
- **Stripe** para pagamentos

### **Infraestrutura**
- **Docker** para containerização
- **PostgreSQL** para produção
- **Redis** para cache e filas
- **Nginx** para proxy reverso

## 📦 **Instalação e Execução**

### **Pré-requisitos**
- Node.js 18+
- Python 3.11+
- Docker e Docker Compose

### **1. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/snaplinked.git
cd snaplinked
```

### **2. Configuração com Docker (Recomendado)**
```bash
# Inicie todos os serviços
docker-compose up -d

# A aplicação estará disponível em:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### **3. Configuração Manual**

#### **Backend**
```bash
cd snaplinked-backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Executar migrações
flask db upgrade

# Iniciar servidor
python src/main.py
```

#### **Frontend**
```bash
cd snaplinked-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Build para produção
npm run build
```

## 🔧 **Configuração**

### **Variáveis de Ambiente**

#### **Backend (.env)**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/snaplinked

# JWT
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Redis
REDIS_URL=redis://localhost:6379

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### **Frontend (.env)**
```env
VITE_API_URL=http://localhost:5000/api
VITE_STRIPE_PUBLIC_KEY=pk_test_...
```

## 📚 **Documentação da API**

### **Autenticação**
```bash
# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

# Registro
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "password",
  "first_name": "João",
  "last_name": "Silva"
}
```

### **Automações**
```bash
# Listar automações
GET /api/automations

# Criar automação
POST /api/automations
{
  "name": "Tech Outreach",
  "type": "connection_request",
  "target_keywords": ["developer", "engineer"],
  "message_template": "Hi {name}!",
  "daily_limit": 50
}

# Ativar/Pausar automação
POST /api/automations/{id}/toggle
```

### **Analytics**
```bash
# Obter analytics
GET /api/analytics?range=7d

# Exportar dados
GET /api/analytics/export?format=csv
```

## 🏗️ **Arquitetura**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   Flask API     │    │   PostgreSQL    │
│                 │    │                 │    │                 │
│ • Dashboard     │◄──►│ • REST API      │◄──►│ • User Data     │
│ • Automations   │    │ • Authentication│    │ • Automations   │
│ • Analytics     │    │ • Background    │    │ • Analytics     │
│ • Settings      │    │   Tasks         │    │ • Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         └──────────────►│                 │◄─────────────┘
                        │ • Sessions      │
                        │ • Cache         │
                        │ • Task Queue    │
                        └─────────────────┘
```

## 🔒 **Segurança**

- **Autenticação JWT** com refresh tokens
- **Criptografia** de senhas com bcrypt
- **Rate Limiting** para APIs
- **CORS** configurado adequadamente
- **Validação** de entrada em todas as rotas
- **Logs de Auditoria** para ações críticas

## 📈 **Performance**

- **Lazy Loading** de componentes React
- **Caching** inteligente com Redis
- **Otimização** de queries SQL
- **Compressão** de assets estáticos
- **CDN** para recursos estáticos

## 🧪 **Testes**

```bash
# Testes do Backend
cd snaplinked-backend
pytest tests/

# Testes do Frontend
cd snaplinked-frontend
npm test

# Testes E2E
npm run test:e2e
```

## 🚀 **Deploy**

### **Produção com Docker**
```bash
# Build das imagens
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### **Deploy Manual**
1. Configure um servidor com Python 3.11+ e Node.js 18+
2. Configure PostgreSQL e Redis
3. Clone o repositório
4. Configure as variáveis de ambiente
5. Execute o build do frontend
6. Inicie o backend com Gunicorn
7. Configure Nginx como proxy reverso

## 📊 **Monitoramento**

- **Health Checks** automáticos
- **Logs Estruturados** com níveis
- **Métricas** de performance
- **Alertas** para falhas críticas

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 **Autor**

**Manus AI** - Desenvolvimento completo do SnapLinked

- 🌐 **Demo**: [https://kkh7ikc7v7gg.manus.space](https://kkh7ikc7v7gg.manus.space)
- 📧 **Contato**: [Suporte Manus](https://help.manus.im)

## 🙏 **Agradecimentos**

- React Team pelo framework incrível
- Flask Team pela simplicidade e flexibilidade
- Tailwind CSS pela produtividade em estilização
- Shadcn/ui pelos componentes elegantes

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
