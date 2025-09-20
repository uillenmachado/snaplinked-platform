# SnapLinked Platform

Sistema profissional de automação LinkedIn com arquitetura limpa e modular.

## 🚀 Início Rápido

### Requisitos
- Python 3.12+
- Node.js 20+
- Docker e Docker Compose (opcional)
- pnpm (gerenciador de pacotes para o frontend)

### Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/uillenmachado/snaplinked-platform.git
cd snaplinked-platform
```

2. Configure o backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. Configure o frontend:
```bash
cd frontend
pnpm install
```

4. Configure as variáveis de ambiente:
- Backend: Copie `.env.example` para `.env` e ajuste as configurações
- Frontend: Copie `.env.example` para `.env` e ajuste as configurações

### Executando o Projeto

#### Desenvolvimento Local

1. Backend (em um terminal):
```bash
cd backend
source venv/bin/activate
python src/app.py
```

2. Frontend (em outro terminal):
```bash
cd frontend
pnpm dev
```

#### Usando Docker

```bash
docker-compose up --build
```

O sistema estará disponível em:
- Frontend: http://localhost:3000
- API Backend: http://localhost:5001

## Nova Estrutura do Repositório

### Backend

```
├── src/                  # Código-fonte principal
│   ├── api/             # Endpoints da API
│   ├── auth/            # Autenticação e autorização
│   ├── config/          # Configurações do sistema
│   ├── core/            # Lógica de negócio central
│   ├── database/        # Camada de acesso a dados
│   ├── linkedin/        # Integração com LinkedIn
│   ├── services/        # Serviços da aplicação
│   └── utils/           # Utilitários e helpers
├── tests/               # Testes automatizados
│   ├── unit/           # Testes unitários
│   └── integration/     # Testes de integração
└── requirements.txt     # Dependências Python
```

### Frontend

```
├── src/                 # Código-fonte principal
│   ├── components/      # Componentes React
│   ├── contexts/        # Contexts da aplicação
│   ├── hooks/          # Custom hooks
│   ├── pages/          # Páginas da aplicação
│   ├── services/       # Serviços e API
│   └── utils/          # Utilitários
├── public/             # Assets públicos
└── package.json        # Dependências Node.js
```

### Deploy

```
├── docker/             # Configurações Docker
├── nginx/             # Configurações NGINX
└── scripts/           # Scripts de deploy
```

### Docs

```
├── pt/                # Documentação em Português
└── en/               # Documentação em Inglês
```

O SnapLinked é um micro SaaS de automação para LinkedIn, projetado para ajudar profissionais de vendas, marketing e recrutamento a escalar seu networking de forma inteligente e segura. A plataforma automatiza tarefas repetitivas como envio de convites, mensagens personalizadas e visualização de perfis, permitindo que você foque em construir relacionamentos significativos.

## ✨ Funcionalidades

*   **Autenticação Segura:** Suporte para login via OAuth 2.0 (API oficial) e login manual para automações completas.
*   **Automações Inteligentes:** Envie convites de conexão, visualize perfis e envie mensagens personalizadas de forma automatizada.
*   **Dashboard Completo:** Monitore o desempenho de suas automações com métricas detalhadas e gráficos intuitivos.
*   **Scripts Avançados:** Utilize scripts pré-construídos para executar automações diretamente no console do LinkedIn.
*   **Configurações Flexíveis:** Personalize limites diários, horários de funcionamento e delays para simular comportamento humano e garantir a segurança da sua conta.
*   **Interface Moderna:** Design profissional, responsivo e 100% em português do Brasil.

## 🚀 Tecnologias Utilizadas

*   **Backend:** Python, Flask, Playwright
*   **Frontend:** React, Vite, Tailwind CSS, shadcn/ui
*   **Banco de Dados:** SQLite (para desenvolvimento e testes)
*   **Containerização:** Docker, Docker Compose

## 🏁 Começando

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

*   Node.js (v18 ou superior)
*   Python (v3.10 ou superior)
*   Pip (gerenciador de pacotes Python)
*   Docker e Docker Compose (opcional, para deploy)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Instale as dependências do backend:**

    ```bash
    cd snaplinked-backend
    pip install -r requirements.txt
    ```

3.  **Instale as dependências do frontend:**

    ```bash
    cd ../snaplinked-frontend
    npm install --legacy-peer-deps
    ```

### Configuração

1.  **Crie e configure o arquivo `.env` na raiz do projeto:**

    ```bash
    cp .env.example .env
    ```

2.  **Preencha as variáveis de ambiente no arquivo `.env` com suas credenciais de produção:**

    ```
    # Credenciais LinkedIn
    LINKEDIN_CLIENT_ID=sua-client-id
    LINKEDIN_CLIENT_SECRET=seu-client-secret
    LINKEDIN_REDIRECT_URI=https://snaplinked.com/auth/linkedin/callback

    # Outras configurações...
    ```

### Configuração Adicional

1. **Chave Secreta**:
   - Certifique-se de definir a variável de ambiente `SECRET_KEY` para maior segurança.
   - Exemplo de configuração no arquivo `.env`:
     ```
     SECRET_KEY=sua-chave-secreta-segura
     ```

2. **Configuração do OAuth para LinkedIn**:
   - Preencha as seguintes variáveis no arquivo `.env`:
     ```
     LINKEDIN_CLIENT_ID=sua-client-id
     LINKEDIN_CLIENT_SECRET=sua-client-secret
     LINKEDIN_REDIRECT_URI=http://localhost:5000/callback
     ```

### Executando a Aplicação

1.  **Inicie o servidor backend:**

    ```bash
    cd snaplinked-backend
    python main.py
    ```

2.  **Inicie o servidor frontend em um novo terminal:**

    ```bash
    cd snaplinked-frontend
    npm run dev
    ```

3.  **Acesse a aplicação em seu navegador:**

    [http://localhost:3000](http://localhost:3000)

### Executando Testes Automatizados

1. **Testes do Backend**:
   - Para executar todos os testes automatizados, use o comando:
     ```bash
     cd snaplinked-backend
     pytest tests
     ```

## 🐳 Deploy com Docker

Para fazer o deploy da aplicação em produção utilizando Docker, siga os passos abaixo:

1.  **Construa as imagens e inicie os containers:**

    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```

2.  **Acesse a aplicação em seu navegador:**

    [http://localhost](http://localhost)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

