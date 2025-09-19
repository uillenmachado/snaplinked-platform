# 🚀 SnapLinked - Plataforma de Automação para LinkedIn

**Escale seu networking no LinkedIn com uma plataforma de automação inteligente, segura e pronta para produção.**

[![Versão](https://img.shields.io/badge/versão-4.1.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Status](https://img.shields.io/badge/status-estável-green.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Licença](https://img.shields.io/badge/licença-MIT-green.svg)](LICENSE)

---

## 📋 Sobre o Projeto

O **SnapLinked** é uma plataforma SaaS (Software as a Service) robusta e escalável, projetada para automatizar e otimizar estratégias de networking no LinkedIn. A ferramenta permite que profissionais de vendas, marketing e recrutamento expandam suas redes de contatos de forma eficiente, enviando convites de conexão e mensagens personalizadas em larga escala.

Com uma arquitetura moderna e focada em segurança, o SnapLinked simula o comportamento humano para garantir a conformidade com as políticas do LinkedIn e proteger a conta do usuário. A interface é intuitiva, 100% em português e oferece um dashboard completo com analytics para monitoramento de performance em tempo real.

### ✨ Funcionalidades Principais

*   **Dashboard Analítico**: Visualize métricas de performance, como convites enviados, taxa de aceitação e engajamento, em um painel de controle centralizado.
*   **Automação de Conexões**: Crie e gerencie campanhas para enviar solicitações de conexão personalizadas com base em palavras-chave e perfis de público-alvo.
*   **Login Manual Seguro**: Conecte sua conta LinkedIn de forma segura para habilitar automações completas, sem armazenar credenciais permanentemente.
*   **Simulação de Comportamento Humano**: A plataforma opera com delays e limites inteligentes para evitar a detecção e garantir a segurança da conta.
*   **Arquitetura Escalável**: Construído com Docker, o sistema é modular e pronto para deploy em qualquer ambiente de nuvem, suportando alta disponibilidade e escalabilidade.

---

## 🛠️ Arquitetura e Tecnologias

A plataforma é construída sobre uma arquitetura de microsserviços, utilizando Docker para orquestrar os contêineres do frontend, backend, banco de dados e serviços de mensageria.

#### Frontend

| Tecnologia | Versão | Propósito |
|---|---|---|
| React | 18.x | Biblioteca para construção de interfaces de usuário reativas. |
| Vite | 6.x | Ferramenta de build e servidor de desenvolvimento de alta performance. |
| Tailwind CSS | 4.x | Framework CSS para design rápido e responsivo. |
| Shadcn/ui | Latest | Coleção de componentes de UI acessíveis e customizáveis. |
| React Router | 7.x | Roteamento declarativo para Single-Page Applications (SPA). |

#### Backend

| Tecnologia | Versão | Propósito |
|---|---|---|
| Python | 3.11+ | Linguagem principal para a lógica de negócio e API. |
| Flask | 2.3.x | Microframework web para a construção da API RESTful. |
| PostgreSQL | 15+ | Banco de dados relacional para persistência de dados. |
| Redis | 7+ | Armazenamento em memória para caching e filas de tarefas. |
| PyJWT | 2.8.x | Implementação de JSON Web Tokens para autenticação segura. |

---

## 🚀 Deploy e Execução

A maneira mais simples e recomendada de executar o projeto é utilizando Docker e Docker Compose.

### Pré-requisitos

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Execução com Docker Compose

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/uillenmachado/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Inicie os serviços:**
    Execute o comando a seguir na raiz do projeto para construir as imagens e iniciar todos os contêineres em modo "detached" (-d).
    ```bash
    docker-compose up --build -d
    ```

3.  **Acesse a aplicação:**
    *   O **Frontend** estará disponível em `http://localhost:3000`.
    *   A **API do Backend** estará disponível em `http://localhost:5000`.

Para parar todos os serviços, execute:
```bash
docker-compose down
```

### Execução Manual (Alternativa)

Caso prefira executar os serviços manualmente, siga os passos abaixo.

1.  **Inicie o Backend:**
    ```bash
    cd snaplinked-backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/main.py
    ```

2.  **Inicie o Frontend (em outro terminal):**
    ```bash
    cd snaplinked-frontend
    npm install
    npm run dev
    ```

---

## 🤝 Contribuição

Contribuições são muito bem-vindas! Se você deseja melhorar o projeto, por favor, faça um fork do repositório, crie uma nova branch para sua feature e abra um Pull Request detalhado com suas alterações.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

