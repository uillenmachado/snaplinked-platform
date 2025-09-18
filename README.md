# SnapLinked - Plataforma de Automação LinkedIn

## 🚀 Versão Final Auditada - v3.0.0

**SnapLinked** é uma plataforma SaaS completa para automação de ações no LinkedIn através de scripts JavaScript executados no console do navegador. A solução combina autenticação OAuth 2.0 oficial do LinkedIn com scripts de automação seguros e eficientes.

## ✨ Funcionalidades Principais

### 🔐 Autenticação LinkedIn Real
- **OAuth 2.0 oficial** do LinkedIn
- **Scopes limitados**: `openid`, `profile`, `email` (apenas dados básicos)
- **Conexão segura** com contas LinkedIn reais
- **Proteção CSRF** com state validation

### 🤖 Sistema de Automação via Scripts
- **Scripts JavaScript** para execução no console (F12)
- **Automação de conexões** com mensagens personalizadas
- **Visualização de perfis** estratégica
- **Envio de mensagens** para conexões existentes
- **Delays aleatórios** para simular comportamento humano
- **Limites de segurança** configuráveis

### 📊 Interface Completa
- **Dashboard interativo** com estatísticas em tempo real
- **Gerenciamento de automações** configuráveis
- **Analytics avançados** com gráficos e insights
- **Página de scripts** com códigos prontos para uso
- **Sistema de planos** e assinaturas
- **Interface 100% em português brasileiro**

## 🏗️ Arquitetura Técnica

### Frontend (React + Vite)
```
src/
├── components/
│   ├── layout/DashboardLayout.jsx
│   └── ui/                     # Componentes reutilizáveis
├── pages/
│   ├── DashboardPage.jsx       # Dashboard principal
│   ├── AutomationsPage.jsx     # Gerenciamento de automações
│   ├── LinkedInAccountsPage.jsx # Conexão OAuth LinkedIn
│   ├── AnalyticsPage.jsx       # Estatísticas e gráficos
│   ├── ScriptsPage.jsx         # Scripts de automação
│   └── SettingsPage.jsx        # Configurações
├── scripts/
│   └── linkedin-automation.js  # Scripts de automação
└── services/
    └── api.js                  # Cliente API
```

### Backend (Flask)
```
src/
└── main.py                     # Aplicação Flask completa
```

**Endpoints Principais:**
- `GET /api/health` - Health check
- `POST /api/auth/login` - Login demo
- `GET /api/auth/linkedin/connect` - Iniciar OAuth LinkedIn
- `GET /api/auth/linkedin/callback` - Callback OAuth
- `GET /api/linkedin/profile` - Dados do perfil conectado
- `GET /api/automations` - Lista de automações
- `GET /api/analytics` - Estatísticas de uso
- `GET /scripts/linkedin-automation.js` - Script de automação

## 🛠️ Como Usar

### 1. Acesso à Plataforma
1. Acesse: **https://19hninc0ejo1.manus.space**
2. Faça login com: `demo@snaplinked.com` / `demo123`

### 2. Conectar LinkedIn
1. Vá para **"Contas LinkedIn"** no menu
2. Clique em **"Conectar LinkedIn"**
3. Autorize o SnapLinked no LinkedIn oficial
4. Sua conta será conectada com dados reais

### 3. Executar Automações
1. Vá para **"Scripts"** no menu
2. Copie o script desejado
3. Abra o LinkedIn em nova aba
4. Pressione **F12** para abrir o console
5. Cole e execute o script
6. Monitore a execução através dos logs

### 4. Comandos de Automação

**Conectar por palavra-chave:**
```javascript
conectarPorPalavraChave("desenvolvedor", 25, "Olá! Gostaria de me conectar.");
```

**Visualizar perfis:**
```javascript
visualizarPerfis("CEO startup", 50);
```

**Parar automação:**
```javascript
pararAutomacao();
```

**Ver estatísticas:**
```javascript
estatisticas();
```

## 🔒 Segurança e Boas Práticas

### Proteções Implementadas
- **Rate limiting** automático
- **Delays aleatórios** entre ações (2-5 segundos)
- **Limites diários** configuráveis
- **Detecção de erros** com parada automática
- **Simulação de comportamento humano**

### Limites Recomendados
- **Conexões**: Máximo 50 por dia
- **Mensagens**: Máximo 25 por dia
- **Visualizações**: Máximo 100 por dia
- **Intervalo**: 2-5 segundos entre ações

## 📦 Instalação Local

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- Git

### Frontend
```bash
cd snaplinked-frontend
npm install
npm run dev
```

### Backend
```bash
cd snaplinked-backend
pip install -r requirements.txt
python src/main.py
```

## 🌐 Deploy em Produção

### Variáveis de Ambiente
```bash
SECRET_KEY=your-secret-key
LINKEDIN_CLIENT_ID=77jmwin70p0gqe
LINKEDIN_CLIENT_SECRET=your-client-secret
LINKEDIN_REDIRECT_URI=https://yourdomain.com/api/auth/linkedin/callback
```

### Docker (Opcional)
```bash
docker-compose up -d
```

## 📊 Planos de Assinatura

### Starter - R$ 29/mês
- 5 scripts de automação
- 100 conexões/dia
- 50 mensagens/dia
- Suporte por email

### Professional - R$ 79/mês ⭐
- 20 scripts de automação
- 300 conexões/dia
- 150 mensagens/dia
- Scripts personalizados
- Suporte prioritário

### Enterprise - R$ 199/mês
- Scripts ilimitados
- 1000 conexões/dia
- 500 mensagens/dia
- Scripts customizados
- Suporte dedicado
- Treinamento personalizado

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Email**: suporte@snaplinked.com
- **Documentação**: https://docs.snaplinked.com
- **Issues**: https://github.com/uillenmachado/snaplinked-platform/issues

## 🔄 Changelog

### v3.0.0 - Versão Final Auditada
- ✅ Sistema de scripts JavaScript para automação
- ✅ OAuth 2.0 real do LinkedIn (apenas dados básicos)
- ✅ Interface 100% em português brasileiro
- ✅ Layout responsivo e profissional
- ✅ Página de scripts com códigos prontos
- ✅ Backend simplificado e otimizado
- ✅ Remoção de arquivos desnecessários
- ✅ Documentação completa

### v2.0.0 - Integração LinkedIn Real
- ✅ OAuth 2.0 do LinkedIn implementado
- ✅ Conexão com contas reais
- ✅ Interface traduzida para português
- ✅ Layout corrigido e alinhado

### v1.0.0 - Versão Beta
- ✅ Interface básica funcional
- ✅ Sistema de automação simulado
- ✅ Dashboard e páginas principais

---

**Desenvolvido com ❤️ pela equipe SnapLinked**

*Automatize seu LinkedIn de forma inteligente e segura!*
