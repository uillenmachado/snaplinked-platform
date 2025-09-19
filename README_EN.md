# 🚀 SnapLinked - LinkedIn Automation Platform

**Scale your LinkedIn networking with an intelligent, secure, and production-ready automation platform.**

[![Version](https://img.shields.io/badge/version-4.2.0-blue.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![Status](https://img.shields.io/badge/status-stable-green.svg)](https://github.com/uillenmachado/snaplinked-platform)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 About the Project

**SnapLinked** is a robust and scalable SaaS (Software as a Service) platform designed to automate and optimize LinkedIn networking strategies. The tool enables sales, marketing, and recruitment professionals to efficiently expand their contact networks by sending personalized connection requests and messages at scale.

With a modern, security-focused architecture, SnapLinked uses both the official LinkedIn API for secure authentication and a human-like automation engine for other tasks, ensuring compliance with LinkedIn's policies and protecting the user's account. The interface is intuitive, 100% in Portuguese, and offers a comprehensive dashboard with real-time analytics for performance monitoring.

### ✨ Key Features

*   **Analytics Dashboard**: View performance metrics such as connection requests sent, acceptance rate, and engagement on a centralized dashboard.
*   **Connection Automation**: Create and manage campaigns to send personalized connection requests based on keywords and target audience profiles.
*   **Secure LinkedIn Connection**: Connect your LinkedIn account securely using OAuth 2.0 for authentication or via manual login for full automation capabilities.
*   **Human Behavior Simulation**: The automation engine operates with intelligent delays and limits to avoid detection and ensure account safety.
*   **Scalable Architecture**: Built with Docker, the system is modular and ready for deployment in any cloud environment, supporting high availability and scalability.

---

## 🛠️ Architecture and Technologies

The platform is built on a microservices architecture, using Docker to orchestrate the frontend, backend, database, and messaging services containers.

#### Frontend

| Technology | Version | Purpose |
|---|---|---|
| React | 19.x | A JavaScript library for building reactive user interfaces. |
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
| Playwright | 1.40.x | For browser automation tasks. |

---

## 🚀 Deployment and Execution

The simplest and recommended way to run the project is using Docker and Docker Compose.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Configuration

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/uillenmachado/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Create the environment file:**
    Copy the `.env.example` file to a new file named `.env` and fill in your credentials.
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your real data, especially the LinkedIn and Gemini API keys.

    ```
    # .env file
    LINKEDIN_CLIENT_ID=your_linkedin_client_id
    LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
    LINKEDIN_REDIRECT_URI=http://localhost:3000/auth/linkedin/callback
    GEMINI_API_KEY=your_gemini_api_key
    ...
    ```

3.  **Create the frontend environment file:**
    Create a `.env` file in the `snaplinked-frontend` directory.
    ```bash
    cd snaplinked-frontend
    touch .env
    ```
    Add the following content to `snaplinked-frontend/.env`:
    ```
    VITE_API_URL=http://localhost:5000
    VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
    VITE_LINKEDIN_REDIRECT_URI=http://localhost:3000/auth/linkedin/callback
    NODE_ENV=development
    ```

### Execution with Docker Compose

1.  **Start the services:**
    From the project root, run the following command to build the images and start all containers in detached mode (`-d`).
    ```bash
    docker-compose up --build -d
    ```

2.  **Access the application:**
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
    pip install -r requirements.txt
    playwright install
    python src/main.py
    ```

2.  **Start the Frontend (in another terminal):**
    ```bash
    cd snaplinked-frontend
    npm install --legacy-peer-deps
    npm run dev
    ```

---

## 🤝 Contribution

Contributions are very welcome! If you wish to improve the project, please fork the repository, create a new branch for your feature, and open a detailed Pull Request with your changes.

## 📝 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

