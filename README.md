# SnapLinked - Plataforma de Automação LinkedIn

![SnapLinked Logo](https://img.shields.io/badge/SnapLinked-LinkedIn%20Automation-blue?style=for-the-badge&logo=linkedin)
![Version](https://img.shields.io/badge/version-2.0-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-production%20ready-brightgreen?style=for-the-badge)

**SnapLinked** é uma plataforma SaaS completa para automação de networking no LinkedIn, desenvolvida com tecnologias modernas e foco em funcionalidade real, experiência do usuário e performance.

## 🌐 **Demonstração ao Vivo**

🚀 **[Acesse a Aplicação](https://w5hni7cp6p81.manus.space)**

**Credenciais de Teste:**
- Email: `demo@snaplinked.com`
- Senha: `demo123`

## ✨ **Funcionalidades Principais**

### 🤖 **Automação LinkedIn Real**
- **Login Automático** no LinkedIn com Playwright
- **Busca Inteligente** de pessoas por palavras-chave e localização
- **Solicitações de Conexão** automatizadas com mensagens personalizadas
- **Mensagens de Follow-up** com templates dinâmicos
- **Visualizações de Perfil** estratégicas para aumentar visibilidade
- **Agendamento Inteligente** com horários otimizados
- **Limites de Segurança** para evitar restrições do LinkedIn

### 📊 **Analytics Avançados**
- **Dashboard em Tempo Real** com métricas detalhadas
- **Gráficos Interativos** de performance
- **Insights Automatizados** e recomendações
- **Relatórios Exportáveis** em múltiplos formatos
- **Análise de Palavras-chave** mais eficazes
- **Monitoramento de Taxa de Sucesso**

### 👥 **Gerenciamento de Contas**
- **Múltiplas Contas LinkedIn** em uma interface
- **Verificação Automática** de status das contas
- **Monitoramento de Limites** diários e mensais
- **Rotação Inteligente** entre contas
- **Proteção Anti-Detecção**

### ⚙️ **Configurações Avançadas**
- **Interface 100% em Português BR**
- **Perfil Personalizado** com informações completas
- **Notificações Configuráveis** (email e push)
- **Segurança Robusta** com autenticação JWT
- **Automação Customizável** com delays e horários
- **Templates de Mensagem** pré-definidos

## 🛠️ **Tecnologias Utilizadas**

### **Frontend**
- **React 18** com Hooks e Context API
- **Vite** para build otimizado e desenvolvimento rápido
- **Tailwind CSS** para estilização moderna
- **Shadcn/ui** para componentes elegantes
- **Lucide React** para ícones consistentes
- **React Router** para navegação SPA

### **Backend**
- **Flask** (Python) para API REST robusta
- **SQLAlchemy** para ORM e gerenciamento de dados
- **JWT** para autenticação segura
- **Celery** para tarefas assíncronas
- **Playwright** para automação web real
- **Stripe** para processamento de pagamentos

### **Automação**
- **Playwright** para controle real do navegador
- **Delays Aleatórios** para simular comportamento humano
- **User-Agent Rotation** para evitar detecção
- **Proxy Support** para múltiplas localizações
- **Session Management** para persistência de login

### **Infraestrutura**
- **Docker** para containerização
- **PostgreSQL** para produção
- **Redis** para cache e filas de tarefas
- **Nginx** para proxy reverso

## 📦 **Instalação e Execução**

### **Pré-requisitos**
- Node.js 18+
- Python 3.11+
- Docker e Docker Compose (opcional)

### **1. Clone o Repositório**
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform
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

# LinkedIn (para automação)
LINKEDIN_EMAIL=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password

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

### **Automações Reais**
```bash
# Executar automação LinkedIn
POST /api/real-automation/execute
{
  "name": "Outreach Desenvolvedores",
  "type": "connection_request",
  "linkedin_email": "seu-email@linkedin.com",
  "linkedin_password": "sua-senha",
  "target_keywords": ["desenvolvedor", "programador"],
  "target_location": "Brasil",
  "daily_limit": 50,
  "message_template": "Olá {name}, gostaria de me conectar!"
}

# Verificar status da automação
GET /api/real-automation/status/{automation_id}

# Listar automações ativas
GET /api/real-automation/active
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
│ • Automações    │    │ • Autenticação  │    │ • Automações    │
│ • Analytics     │    │ • Tarefas       │    │ • Analytics     │
│ • Configurações │    │   Assíncronas   │    │ • Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         └──────────────►│                 │◄─────────────┘
                        │ • Sessões       │
                        │ • Cache         │
                        │ • Fila Tarefas  │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Playwright    │
                        │                 │
                        │ • Automação     │
                        │   LinkedIn      │
                        │ • Navegador     │
                        │   Real          │
                        └─────────────────┘
```

## 🔒 **Segurança e Conformidade**

### **Proteções Implementadas**
- **Autenticação JWT** com refresh tokens
- **Criptografia** de senhas com bcrypt
- **Rate Limiting** para APIs
- **CORS** configurado adequadamente
- **Validação** de entrada em todas as rotas
- **Logs de Auditoria** para ações críticas

### **Segurança LinkedIn**
- **Delays Aleatórios** entre ações (30-120 segundos)
- **Limites Diários** configuráveis e seguros
- **Horários Comerciais** para execução
- **User-Agent Real** para evitar detecção
- **Comportamento Humano** simulado
- **Monitoramento** de restrições de conta

## 📈 **Performance**

- **Lazy Loading** de componentes React
- **Caching** inteligente com Redis
- **Otimização** de queries SQL
- **Compressão** de assets estáticos
- **CDN** para recursos estáticos
- **Execução Assíncrona** de automações

## 🧪 **Testes**

```bash
# Testes do Backend
cd snaplinked-backend
pytest tests/

# Testes do Frontend
cd snaplinked-frontend
npm test

# Teste de Automação LinkedIn
python src/linkedin_automation.py
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
- **Dashboard** de monitoramento
- **Relatórios** de execução

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 **Autor**

**Manus AI** - Desenvolvimento completo do SnapLinked

- 🌐 **Demo**: [https://w5hni7cp6p81.manus.space](https://w5hni7cp6p81.manus.space)
- 📧 **Contato**: [Suporte Manus](https://help.manus.im)
- 💼 **GitHub**: [uillenmachado/snaplinked-platform](https://github.com/uillenmachado/snaplinked-platform)

## 🙏 **Agradecimentos**

- React Team pelo framework incrível
- Flask Team pela simplicidade e flexibilidade
- Tailwind CSS pela produtividade em estilização
- Shadcn/ui pelos componentes elegantes
- Playwright pela automação web robusta

## 📋 **Roadmap**

### **v2.1 (Próxima Versão)**
- [ ] Integração com API oficial do LinkedIn
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard de administração
- [ ] Relatórios avançados em PDF
- [ ] Integração com CRM

### **v2.2 (Futuro)**
- [ ] Aplicativo móvel
- [ ] Inteligência artificial para otimização
- [ ] Integração com outras redes sociais
- [ ] API pública para desenvolvedores

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no GitHub!**

🚀 **SnapLinked v2.0 - Automação LinkedIn Real e Profissional**
