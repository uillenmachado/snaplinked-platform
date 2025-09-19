# 🚀 SnapLinked - Plataforma de Automação para LinkedIn

**Automatize seu networking no LinkedIn com inteligência artificial.**

[![Versão](https://img.shields.io/badge/versão-4.1.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Licença](https://img.shields.io/badge/licença-MIT-green.svg)](LICENSE)

## 📋 Sobre o Projeto

O **SnapLinked** é uma plataforma SaaS para automação de networking no LinkedIn. O objetivo é fornecer uma ferramenta inteligente para expandir a rede profissional de forma segura e eficiente, simulando o comportamento humano para garantir a segurança da conta.

### ✨ Funcionalidades Planejadas

*   **Automação Inteligente**: Envio automático de convites de conexão e mensagens personalizadas.
*   **Analytics Avançados**: Dashboard com métricas de performance em tempo real.
*   **Segurança**: Limites configuráveis e simulação de comportamento humano.
*   **Interface Moderna**: Design responsivo e intuitivo em português.

## 🛠️ Tecnologias Utilizadas

#### Frontend

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| React | 18.x | Biblioteca JavaScript para UI |
| Vite | 6.x | Build tool e dev server |
| Tailwind CSS | 4.x | Framework CSS utilitário |
| Shadcn/ui | Latest | Componentes UI profissionais |
| React Router | 7.x | Roteamento SPA |

#### Backend

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.11+ | Linguagem de programação |
| Flask | 2.3.3 | Framework web |
| Playwright | 1.40.0 | Automação de navegador |
| PyJWT | 2.8.0 | Autenticação JWT |
| SQLite | Latest | Banco de dados local |

## 🚀 Como Executar

### Pré-requisitos

*   Node.js 18+
*   Python 3.11+
*   Git

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/uillenmachado/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Configure o Backend:**
    ```bash
    cd snaplinked-backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install
    # Crie um arquivo .env a partir do .env.example e preencha as variáveis
    cp .env.example .env 
    ```

3.  **Configure o Frontend:**
    ```bash
    cd ../snaplinked-frontend
    npm install --legacy-peer-deps
    ```

### Execução

1.  **Inicie o Backend:**
    ```bash
    cd snaplinked-backend
    source venv/bin/activate
    python main.py
    ```

2.  **Inicie o Frontend (em outro terminal):**
    ```bash
    cd snaplinked-frontend
    npm run dev
    ```

A aplicação estará disponível em `http://localhost:3000`.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir, faça um fork do repositório, crie uma nova branch para sua feature e abra um Pull Request detalhado.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

