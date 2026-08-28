# Local Development Environment Setup Guide

---

## 1. Prerequisites
- Docker Engine 24.0+ & Docker Compose 2.20+
- JDK 17+ (for backend local execution)
- Node.js 18+ / pnpm 8+ (for frontend local execution)
- Python 3.11+ & `uv` package manager (for AI workspace execution)

---

## 2. Environment Setup

1. Clone the repository and copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Boot the core local infrastructure stack (PostgreSQL, Redis, Kafka):
   ```bash
   docker-compose up -d postgres redis kafka zookeeper
   ```

3. Verify running containers:
   ```bash
   docker-compose ps
   ```

4. Start individual workspace services:
   - Backend: `./mvnw spring-boot:run` or `gradle bootRun` inside `backend/`
   - Frontend: `npm run dev` inside `frontend/`
   - AI Service: `uvicorn main:app --reload` inside `ai/`
