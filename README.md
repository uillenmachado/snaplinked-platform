# 🚀 SnapLinked - Automação Profissional LinkedIn

Uma plataforma completa de automação para LinkedIn com interface visual integrada.

## ✨ Características

- 🎯 **Dashboard Integrado** - Navegador LinkedIn embutido na interface
- 🤖 **Automação Visual** - Execute ações e veja os resultados em tempo real
- 📊 **Estatísticas Dinâmicas** - Acompanhe curtidas, conexões e comentários
- 🔒 **Seguro e Confiável** - Conexão segura com sua conta LinkedIn
- 🎨 **Interface Moderna** - Design profissional e responsivo

## 🚀 Instalação e Uso

### Requisitos
- Python 3.8+
- Navegador moderno

### Instalação
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform/backend
pip install -r requirements.txt
python app.py
```

### Acesso
- **Dashboard:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

## 📁 Estrutura do Projeto

```
snaplinked-platform/
├── README.md              # Documentação
├── backend/               # Servidor Flask
│   ├── app.py            # Aplicação principal
│   ├── requirements.txt  # Dependências Python
│   └── static/
│       └── index.html    # Dashboard integrado
└── frontend/             # Configuração React
    └── package.json      # Dependências Node.js
```

## 🎯 Como Usar

1. **Conectar LinkedIn** - Clique no botão "🔗 Conectar LinkedIn"
2. **Executar Automações** - Use os botões na sidebar:
   - 👍 **Curtir Posts** - Curte 3 posts automaticamente
   - 🤝 **Enviar Conexões** - Envia 2 solicitações de conexão
   - 💬 **Comentar Posts** - Comenta 1 post automaticamente
3. **Acompanhar Resultados** - Veja as estatísticas atualizarem em tempo real

## 🛡️ Segurança

- Todas as credenciais são mantidas localmente
- Conexão segura com LinkedIn
- Sem armazenamento de dados sensíveis
- Interface isolada em iframe

## 🎨 Interface

O SnapLinked oferece uma experiência visual completa:
- **Header** com status de conexão
- **Sidebar** com controles de automação e estatísticas
- **Área principal** com navegador LinkedIn integrado
- **Overlay de progresso** durante automações

## 📊 Funcionalidades

### Automações Disponíveis
- ✅ Curtir posts no feed
- ✅ Enviar solicitações de conexão
- ✅ Comentar posts com mensagens profissionais
- ✅ Estatísticas em tempo real
- ✅ Interface visual integrada

### APIs Disponíveis
- `GET /api/health` - Verificação de saúde
- `GET /api/status` - Status da aplicação
- `POST /api/connect-linkedin` - Conectar LinkedIn
- `POST /api/automation/{action}` - Executar automação

## 🔧 Desenvolvimento

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (React) - Opcional
```bash
cd frontend
npm install
npm run build
```

## 📝 Licença

Este projeto é privado e proprietário.

---

**SnapLinked v2.0** - Desenvolvido com ❤️ para profissionais que valorizam eficiência e automação inteligente.
