# GitEval.ai 🚀

**GitEval.ai** is an AI-powered system designed to analyze GitHub profiles and provide actionable job-readiness insights. By combining deep LLM analysis with heuristic code quality checks, it simulates a recruiter's perspective and helps developers bridge the gap between "code" and "career."

![Dashboard Mockup](https://raw.githubusercontent.com/Malarselvi05/GitEvaluator/main/frontend/public/next.svg) <!-- Replace with real screenshot if available -->

## ✨ Features

- **Portfolio Scoring (0-100)**: Multi-dimensional analysis of code quality, innovation, documentation, and industry relevance.
- **Recruiter Verdict**: A persona-based AI simulation of a Senior Hiring Manager's 30-second profile scan.
- **Competency Radar**: Visual breakdown of your technical strengths and gaps across frontend, backend, ML, and DevOps.
- **AI Project Builder**: Intelligent recommendations for "what to build next" to maximize your hiring potential.
- **Async Engine**: Powered by Celery and Redis for fast, non-blocking analysis of large repositories.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4 (Glassmorphism design)
- **Animations**: Framer Motion
- **Visualization**: Recharts

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy
- **Task Queue**: Celery + Redis
- **AI Engines**: Anthropic Claude API (Sonnet for analysis, Haiku for classification)

## 📁 Structure

```
github-evaluator/
├── backend/            # FastAPI source, Celery workers, and AI services
├── frontend/           # Next.js source, Tailwind styles, and UI components
├── implementation_plan.md  # Detailed system architecture
└── progress_checklist.md   # Implementation milestones
```

## 🚀 Getting Started

### Prerequisites
- Node.js >= 20
- Python >= 3.11
- Docker (for PostgreSQL & Redis)

### Backend Setup
1. `cd backend`
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env` (Add your API keys)
5. `uvicorn main:app --reload`

### Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Worker Setup (Async Analysis)
1. Ensure Redis is running
2. `cd backend`
3. `celery -A worker.celery_app worker --loglevel=info`

## 📊 Roadmap

- [x] Phase 1: Foundation & Design System
- [x] Phase 2: Core Analysis Engine
- [ ] Phase 3: Performance & Redis Caching
- [ ] Phase 4: GitHub OAuth Integration
- [ ] Phase 5: AI Project Recommendations

---

Built with ❤️ by [Malarselvi05](https://github.com/Malarselvi05)
