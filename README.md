# 🚀 AI-Powered Online Judge (LeetCode Clone)

An advanced, distributed code execution platform and competitive programming judge featuring real-time AI mentoring and Machine Learning-driven problem recommendations.

## ✨ Key Features

* **Distributed Execution Engine**: Securely runs untrusted user code (C++, Java, Python) in isolated, ephemeral Docker containers to enforce strict Time Limit (TLE) and Memory Limit constraints.
* **Asynchronous Task Queue**: Utilizes **Celery** and **Redis** as a message broker to handle high-volume concurrent code submissions without blocking the main API.
* **AI Code Mentor (Groq LLM)**: Analyzes user submissions to provide real-time architectural feedback, Big-O complexity analysis, and automated code reviews.
* **ML 'Learning Sweet-Spot' Recommender**: An **XGBoost** predictive pipeline that analyzes user success rates to recommend problems with an optimal 65% win-probability to maximize learning growth.
* **Dynamic Admin Pipeline**: Complete administrative dashboard for creating problems, writing strict metadata schemas, and dynamically generating massive test-case outputs against optimal reference solutions.

## 🛠️ Tech Stack

* **Frontend**: React, TypeScript, Vite, Tailwind CSS, Monaco Editor
* **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
* **Execution & Async**: Docker, Celery, Redis
* **AI / ML**: XGBoost, Pandas, Groq API (LLM)

## ⚙️ Local Setup & Installation

To run this project locally, you will need **Docker Desktop**, **Node.js**, and **Python 3.9+**.

### 1. Start the Databases (Docker)
Ensure Docker is running, then spin up the PostgreSQL and Redis containers:
`ash
docker-compose up -d
`

### 2. Start the Backend API
Open a terminal, navigate to the backend, configure your virtual environment, and start the FastAPI server:
`ash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
`

### 3. Start the Celery Worker (Code Execution Engine)
Open a **new** terminal, activate the same virtual environment, and start the worker:
`ash
cd backend
# Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
`
*(Note: If you are on Mac/Linux, you can omit the --pool=solo flag)*

### 4. Start the Frontend
Open a **new** terminal, install the dependencies, and run the React app:
`ash
cd frontend
npm install
npm run dev
`

## 🔒 Environment Variables
Make sure to copy the ackend/.env.example file to ackend/.env and add your own GROQ_API_KEY to enable the AI Mentor features.
