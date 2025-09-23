# 🚀 SnapLinked v3.0 - Automação Profissional LinkedIn

Uma plataforma completa de automação para LinkedIn com funcionalidades reais, segurança avançada e interface profissional.

## ✨ Novidades da v3.0

- 🤖 **Automação Real** - Implementação com Playwright para ações reais no LinkedIn
- 🔐 **Segurança Avançada** - OAuth LinkedIn, JWT, criptografia e proteção CSRF
- 💾 **Persistência de Dados** - Banco de dados SQLAlchemy com histórico completo
- 🧪 **Testes Automatizados** - Cobertura completa com testes unitários e de integração
- 🎨 **Interface Otimizada** - Frontend refatorado com separação de arquivos e UX melhorada
- 📊 **Monitoramento** - Logs detalhados e estatísticas em tempo real

## 🎯 Características Principais

- 🔗 **Duas Opções de Login** - OAuth oficial ou login manual
- 👍 **Curtir Posts** - Automação inteligente de curtidas no feed
- 🤝 **Enviar Conexões** - Solicitações automáticas de conexão
- 💬 **Comentar Posts** - Comentários profissionais automatizados
- 📈 **Estatísticas Detalhadas** - Acompanhamento completo de atividades
- 🛡️ **Segurança Total** - Proteção contra vulnerabilidades conhecidas

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- Node.js 16+ (opcional, para desenvolvimento frontend)
- Navegador moderno

### 1. Clonar o Repositório
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform/backend
```

### 2. Configurar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Inicializar Banco de Dados
```bash
python init_db.py init
```

### 6. Executar Aplicação
```bash
python app.py
```

### 7. Acessar Dashboard
Abra seu navegador em: http://localhost:5000

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Configurações Flask
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=sua-chave-secreta-aqui

# Banco de dados
DATABASE_URL=sqlite:///snaplinked.db

# LinkedIn API (OAuth)
LINKEDIN_CLIENT_ID=seu-client-id
LINKEDIN_CLIENT_SECRET=seu-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:5000/auth/linkedin/callback

# Configurações de automação
AUTOMATION_DELAY=2
MAX_ACTIONS_PER_SESSION=50
```

### Configuração OAuth LinkedIn

1. Acesse [LinkedIn Developers](https://developer.linkedin.com/)
2. Crie uma nova aplicação
3. Configure as URLs de redirecionamento
4. Copie Client ID e Client Secret para o `.env`

## 📁 Estrutura do Projeto

```
snaplinked-platform/
├── README.md                 # Documentação principal
├── backend/                  # Servidor Flask
│   ├── app.py               # Aplicação principal
│   ├── config.py            # Configurações
│   ├── models.py            # Modelos de dados
│   ├── init_db.py           # Inicialização do BD
│   ├── run_tests.py         # Executor de testes
│   ├── requirements.txt     # Dependências Python
│   ├── .env.example         # Exemplo de configuração
│   ├── services/            # Serviços de negócio
│   │   └── linkedin_service.py
│   ├── static/              # Arquivos estáticos
│   │   ├── css/
│   │   │   └── main.css     # Estilos principais
│   │   ├── js/
│   │   │   └── main.js      # JavaScript principal
│   │   └── index.html       # Interface principal
│   └── tests/               # Testes automatizados
│       ├── test_models.py
│       └── test_api.py
└── frontend/                # Configuração React (opcional)
    └── package.json
```

## 🎮 Como Usar

### 1. Conectar ao LinkedIn

**Opção A: OAuth (Recomendado)**
- Clique em "OAuth LinkedIn"
- Autorize a aplicação no LinkedIn
- Retorne automaticamente autenticado

**Opção B: Login Manual**
- Clique em "Login Manual"
- Insira seu email
- Faça login no LinkedIn na janela que abrir

### 2. Executar Automações

Após conectado, use os botões na sidebar:

- **👍 Curtir 3 Posts** - Curte posts automaticamente no feed
- **🤝 Enviar 2 Conexões** - Envia solicitações de conexão
- **💬 Comentar 1 Post** - Adiciona comentários profissionais

### 3. Acompanhar Estatísticas

- Visualize curtidas, conexões e comentários em tempo real
- Acesse histórico detalhado de ações
- Reset estatísticas quando necessário

## 🧪 Testes

### Executar Todos os Testes
```bash
python run_tests.py
```

### Executar Teste Específico
```bash
python run_tests.py --test tests.test_models.TestModels.test_user_creation
```

### Listar Testes Disponíveis
```bash
python run_tests.py --list
```

### Cobertura de Código
```bash
pip install coverage
python run_tests.py --coverage
```

## 🛠️ Desenvolvimento

### Estrutura de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Executar em modo de desenvolvimento
FLASK_ENV=development python app.py

# Executar testes continuamente
python run_tests.py --watch

# Verificar qualidade do código
pylint backend/
flake8 backend/
bandit -r backend/
```

### Comandos Úteis

```bash
# Gerenciar banco de dados
python init_db.py init     # Inicializar
python init_db.py reset    # Resetar (CUIDADO!)
python init_db.py stats    # Ver estatísticas

# Executar testes
python run_tests.py        # Todos os testes
python run_tests.py -q     # Modo silencioso
python run_tests.py -c     # Com cobertura
```

## 🔒 Segurança

### Medidas Implementadas

- ✅ **Autenticação JWT** - Tokens seguros com expiração
- ✅ **OAuth 2.0** - Integração oficial LinkedIn
- ✅ **Proteção CSRF** - Validação de estado OAuth
- ✅ **Sanitização** - Validação de entrada de dados
- ✅ **HTTPS Ready** - Configuração para produção
- ✅ **Dependências Seguras** - Versões atualizadas

### Configuração de Produção

```env
FLASK_ENV=production
FLASK_DEBUG=false
FLASK_HOST=0.0.0.0
SESSION_COOKIE_SECURE=true
```

## 📊 API Endpoints

### Autenticação
- `GET /api/auth/linkedin` - Iniciar OAuth
- `POST /api/auth/manual-login` - Login manual
- `POST /api/auth/logout` - Logout

### Automação
- `POST /api/automation/like` - Curtir posts
- `POST /api/automation/connect` - Enviar conexões
- `POST /api/automation/comment` - Comentar posts
- `GET /api/automation/sessions` - Histórico de sessões
- `GET /api/automation/logs` - Logs detalhados

### Estatísticas
- `GET /api/status` - Status da aplicação
- `POST /api/stats/reset` - Resetar estatísticas

### Utilitários
- `GET /api/health` - Verificação de saúde

## 🚀 Deploy

### Desenvolvimento Local
```bash
python app.py
```

### Produção com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Changelog

### v3.0.0 (2025-09-23)
- 🎉 **Lançamento da v3.0** - Reescrita completa
- 🤖 Automação real com Playwright
- 🔐 Sistema de autenticação OAuth + JWT
- 💾 Persistência com SQLAlchemy
- 🧪 Testes automatizados completos
- 🎨 Interface otimizada e responsiva
- 🛡️ Correção de vulnerabilidades de segurança

### v2.0.0 (Anterior)
- Interface visual integrada
- Simulação de automações
- Dashboard básico

## 📄 Licença

Este projeto é privado e proprietário.

## 🆘 Suporte

- 📧 Email: suporte@snaplinked.com
- 📚 Documentação: [Wiki do Projeto](https://github.com/uillenmachado/snaplinked-platform/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/uillenmachado/snaplinked-platform/issues)

## ⚠️ Aviso Legal

Este software é destinado apenas para uso educacional e profissional. Use com responsabilidade e respeite os termos de serviço do LinkedIn. Os desenvolvedores não se responsabilizam pelo uso inadequado da ferramenta.

---

**SnapLinked v3.0** - Desenvolvido com ❤️ para profissionais que valorizam automação inteligente e segura.

🌟 **Dê uma estrela no projeto se ele foi útil para você!**
