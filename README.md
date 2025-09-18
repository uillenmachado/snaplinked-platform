# 🚀 SnapLinked - Plataforma de Automação LinkedIn

**Automatize seu networking no LinkedIn com inteligência artificial**

[![Versão](https://img.shields.io/badge/versão-4.1.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Status](https://img.shields.io/badge/status-ativo-green.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Licença](https://img.shields.io/badge/licença-MIT-yellow.svg)](LICENSE)

## 📋 Sobre o Projeto

O **SnapLinked** é uma plataforma SaaS completa para automação de networking no LinkedIn. Desenvolvido com tecnologias modernas, oferece automação inteligente para expandir sua rede profissional de forma segura e eficiente.

### ✨ Funcionalidades Principais

- 🤖 **Automação Inteligente**: Envio automático de solicitações de conexão
- 💬 **Mensagens Personalizadas**: Follow-up automático com mensagens customizadas
- 👁️ **Visualização Estratégica**: Visualização automática de perfis relevantes
- 📊 **Analytics Avançados**: Relatórios detalhados de performance
- 🔒 **Segurança Garantida**: Comportamento humano simulado para proteção da conta
- 🌐 **Interface Moderna**: Design responsivo e intuitivo 100% em português
- 🏗️ **Arquitetura Modular**: Backend refatorado com separação de responsabilidades
- ✅ **Testes Automatizados**: Cobertura completa com testes unitários e de integração
- 🛡️ **Segurança Aprimorada**: Validação robusta, rate limiting e proteção CSRF

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React 18** - Biblioteca JavaScript moderna
- **Vite** - Build tool rápido e eficiente
- **Tailwind CSS** - Framework CSS utilitário
- **React Router** - Roteamento SPA
- **Shadcn/ui** - Componentes UI profissionais

### Backend
- **Flask 2.3.3** - Framework web Python
- **Flask-CORS** - Suporte a CORS
- **Playwright 1.40.0** - Automação de navegador
- **PyJWT 2.8.0** - Autenticação JWT segura
- **Werkzeug 2.3.7** - Utilitários web seguros
- **Pytest 7.4.3** - Framework de testes
- **LinkedIn OAuth 2.0** - Autenticação oficial
- **SQLite** - Banco de dados local

## 🚀 Como Executar

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- Git

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform
```

2. **Configure o Backend**
```bash
cd snaplinked-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Configure o Frontend**
```bash
cd ../snaplinked-frontend
npm install
```

4. **Execute o Projeto**

Backend:
```bash
cd snaplinked-backend
python src/main.py
```

Frontend:
```bash
cd snaplinked-frontend
npm run dev
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório `snaplinked-backend`:

```env
SECRET_KEY=sua-chave-secreta-aqui
LINKEDIN_CLIENT_ID=seu-client-id-linkedin
LINKEDIN_CLIENT_SECRET=seu-client-secret-linkedin
LINKEDIN_REDIRECT_URI=http://localhost:5000/api/auth/linkedin/callback
```

### LinkedIn OAuth 2.0

1. Acesse [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Crie uma nova aplicação
3. Configure os scopes: `openid`, `profile`, `email`
4. Adicione a URL de callback: `http://localhost:5000/api/auth/linkedin/callback`

## 📖 Como Usar

### 1. Acesso ao Sistema
- Acesse a aplicação no navegador
- Faça login com suas credenciais ou use a conta demo:
  - **Email**: demo@snaplinked.com
  - **Senha**: demo123

### 2. Conectar LinkedIn
- Vá para "Contas LinkedIn" no menu lateral
- Escolha entre duas opções:
  - **OAuth 2.0**: Conexão oficial (dados básicos)
  - **Login Manual**: Conexão completa (automações)

### 3. Configurar Automações
- Acesse "Automações" no menu
- Configure palavras-chave de busca
- Defina mensagens personalizadas
- Estabeleça limites diários de segurança

### 4. Executar Automações
- Clique em "Iniciar Automação"
- Monitore o progresso em tempo real
- Visualize estatísticas e resultados

## 🔒 Segurança

### Proteções Implementadas
- **Delays Aleatórios**: Entre 2-5 segundos entre ações
- **Limites Diários**: Máximo 50 conexões e 25 mensagens por dia
- **Comportamento Humano**: Simulação de padrões naturais
- **Detecção de Erros**: Parada automática em caso de problemas
- **Horários Inteligentes**: Execução apenas em horários comerciais

### Boas Práticas
- Use mensagens personalizadas e relevantes
- Mantenha limites conservadores
- Monitore regularmente a performance
- Respeite as políticas do LinkedIn

## 📊 APIs Disponíveis

### Autenticação
- `POST /api/auth/login` - Login do usuário
- `POST /api/auth/register` - Registro de novo usuário
- `POST /api/auth/logout` - Logout do usuário

### LinkedIn
- `GET /api/auth/linkedin/connect` - Iniciar OAuth LinkedIn
- `GET /api/auth/linkedin/callback` - Callback OAuth
- `POST /api/linkedin/manual-login` - Login manual
- `GET /api/linkedin/profile` - Obter perfil conectado
- `POST /api/linkedin/disconnect` - Desconectar conta

### Automações
- `GET /api/automations` - Listar automações
- `POST /api/automations/run` - Executar automação
- `GET /api/automations/stats` - Estatísticas de automação

### Analytics
- `GET /api/analytics` - Dados de analytics
- `GET /api/dashboard/stats` - Estatísticas do dashboard

## 🎨 Interface

### Páginas Principais
- **Landing Page**: Apresentação do produto
- **Login/Registro**: Autenticação de usuários
- **Dashboard**: Visão geral e estatísticas
- **Contas LinkedIn**: Gerenciamento de conexões
- **Automações**: Configuração e execução
- **Analytics**: Relatórios e insights
- **Configurações**: Preferências do usuário

### Design System
- **Cores**: Paleta azul profissional LinkedIn
- **Tipografia**: Fonte Inter para legibilidade
- **Componentes**: Baseados em Shadcn/ui
- **Responsividade**: Mobile-first design
- **Acessibilidade**: Padrões WCAG 2.1

## 🚀 Deploy

### Produção
O projeto está configurado para deploy em plataformas modernas:

- **Frontend**: Vercel, Netlify, ou similar
- **Backend**: Heroku, Railway, ou VPS
- **Banco**: PostgreSQL para produção

### Docker (Opcional)
```bash
# Build das imagens
docker-compose build

# Executar containers
docker-compose up -d
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌐 Demo Online

**Acesse a aplicação funcionando:** [https://3dhkilc8y7yd.manus.space](https://3dhkilc8y7yd.manus.space)

**Credenciais de teste:**
- Email: demo@snaplinked.com
- Senha: demo123

## 📞 Suporte

- **Email**: suporte@snaplinked.com
- **Website**: https://snaplinked.com
- **Documentação**: https://docs.snaplinked.com

## 🏆 Reconhecimentos

- LinkedIn pela API oficial
- Comunidade React e Flask
- Contribuidores do projeto

---

**Desenvolvido com ❤️ por [Uillen Machado](https://github.com/uillenmachado)**

*Transforme seu networking no LinkedIn com automação inteligente!*
