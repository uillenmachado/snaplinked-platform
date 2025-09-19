# 🚀 SnapLinked - LinkedIn Automation Platform

**Scale your LinkedIn networking with an intelligent, secure, and production-ready automation platform.**

[![Version](https://img.shields.io/badge/version-4.1.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Status](https://img.shields.io/badge/status-stable-green.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 About the Project

**SnapLinked** is a robust and scalable SaaS (Software as a Service) platform designed to automate and optimize LinkedIn networking strategies. The tool enables sales, marketing, and recruitment professionals to efficiently expand their contact networks by sending personalized connection requests and messages at scale.

With a modern, security-focused architecture, SnapLinked simulates human behavior to ensure compliance with LinkedIn's policies and protect the user's account. The interface is intuitive, 100% in Portuguese, and offers a comprehensive dashboard with real-time analytics for performance monitoring.

### ✨ Key Features

*   **Analytics Dashboard**: View performance metrics such as connection requests sent, acceptance rate, and engagement on a centralized dashboard.
*   **Connection Automation**: Create and manage campaigns to send personalized connection requests based on keywords and target audience profiles.
*   **Secure Manual Login**: Securely connect your LinkedIn account to enable full automation features without permanently storing credentials.
*   **Human Behavior Simulation**: The platform operates with intelligent delays and limits to avoid detection and ensure account safety.
*   **Scalable Architecture**: Built with Docker, the system is modular and ready for deployment in any cloud environment, supporting high availability and scalability.

---

## 🛠️ Architecture and Technologies

The platform is built on a microservices architecture, using Docker to orchestrate the frontend, backend, database, and messaging services containers.

#### Frontend

| Technology | Version | Purpose |
|---|---|---|
| React | 18.x | A JavaScript library for building reactive user interfaces. |
| Vite | 6.x | A high-performance build tool and development server. |
| Tailwind CSS | 4.x | A utility-first CSS framework for rapid and responsive design. |
| Shadcn/ui | Latest | A collection of accessible and customizable UI components. |
| React Router | 7.x | Declarative routing for Single-Page Applications (SPA). |

#### Backend

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | The primary language for business logic and the API. |
| Flask | 2.3.x | A web microframework for building the RESTful API. |
| PostgreSQL | 15+ | A relational database for data persistence. |
| Redis | 7+ | An in-memory data store for caching and task queues. |
| PyJWT | 2.8.x | An implementation of JSON Web Tokens for secure authentication. |

---

## 🚀 Deployment and Execution

The simplest and recommended way to run the project is using Docker and Docker Compose.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Execution with Docker Compose

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/uillenmachado/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Start the services:**
    Run the following command in the project root to build the images and start all containers in detached mode (-d).
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the application:**
    *   The **Frontend** will be available at `http://localhost:3000`.
    *   The **Backend API** will be available at `http://localhost:5000`.

To stop all services, run:
```bash
docker-compose down
```

### Manual Execution (Alternative)

If you prefer to run the services manually, follow the steps below.

1.  **Start the Backend:**
    ```bash
    cd snaplinked-backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/main.py
    ```

2.  **Start the Frontend (in another terminal):**
    ```bash
    cd snaplinked-frontend
    npm install
    npm run dev
    ```

---

## 🤝 Contribution

Contributions are very welcome! If you wish to improve the project, please fork the repository, create a new branch for your feature, and open a detailed Pull Request with your changes.

## 📝 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

