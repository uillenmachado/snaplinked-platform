# SnapLinked - Automação Inteligente para LinkedIn

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

2.  **Preencha as variáveis de ambiente no arquivo `.env` com suas credenciais:**

    ```
    # Credenciais de teste LinkedIn
    LINKEDIN_TEST_EMAIL=seu-email@exemplo.com
    LINKEDIN_TEST_PASSWORD=sua-senha

    # Outras configurações...
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

