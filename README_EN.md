# SnapLinked - Intelligent Automation for LinkedIn

SnapLinked is a LinkedIn automation micro SaaS designed to help sales, marketing, and recruiting professionals scale their networking intelligently and securely. The platform automates repetitive tasks like sending invitations, personalized messages, and viewing profiles, allowing you to focus on building meaningful relationships.

## ✨ Features

*   **Secure Authentication:** Support for login via OAuth 2.0 (official API) and manual login for full automation.
*   **Intelligent Automations:** Send connection invitations, view profiles, and send personalized messages automatically.
*   **Complete Dashboard:** Monitor the performance of your automations with detailed metrics and intuitive graphs.
*   **Advanced Scripts:** Use pre-built scripts to run automations directly in the LinkedIn console.
*   **Flexible Settings:** Customize daily limits, operating hours, and delays to simulate human behavior and ensure your account's safety.
*   **Modern Interface:** Professional, responsive design, and 100% in Brazilian Portuguese.

## 🚀 Technologies Used

*   **Backend:** Python, Flask, Playwright
*   **Frontend:** React, Vite, Tailwind CSS, shadcn/ui
*   **Database:** SQLite (for development and testing)
*   **Containerization:** Docker, Docker Compose

## 🏁 Getting Started

Follow the steps below to set up and run the project in your local environment.

### Prerequisites

*   Node.js (v18 or higher)
*   Python (v3.10 or higher)
*   Pip (Python package manager)
*   Docker and Docker Compose (optional, for deployment)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/snaplinked-platform.git
    cd snaplinked-platform
    ```

2.  **Install backend dependencies:**

    ```bash
    cd snaplinked-backend
    pip install -r requirements.txt
    ```

3.  **Install frontend dependencies:**

    ```bash
    cd ../snaplinked-frontend
    npm install --legacy-peer-deps
    ```

### Configuration

1.  **Create and configure the `.env` file in the project root:**

    ```bash
    cp .env.example .env
    ```

2.  **Fill in the environment variables in the `.env` file with your credentials:**

    ```
    # LinkedIn test credentials
    LINKEDIN_TEST_EMAIL=your-email@example.com
    LINKEDIN_TEST_PASSWORD=your-password

    # Other settings...
    ```

### Running the Application

1.  **Start the backend server:**

    ```bash
    cd snaplinked-backend
    python main.py
    ```

2.  **Start the frontend server in a new terminal:**

    ```bash
    cd snaplinked-frontend
    npm run dev
    ```

3.  **Access the application in your browser:**

    [http://localhost:3000](http://localhost:3000)

## 🐳 Deploy with Docker

To deploy the application in production using Docker, follow the steps below:

1.  **Build the images and start the containers:**

    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```

2.  **Access the application in your browser:**

    [http://localhost](http://localhost)

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

