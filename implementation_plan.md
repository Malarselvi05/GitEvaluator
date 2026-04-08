# GitHub Project Evaluator — Implementation Plan

> **Project:** GitHub Project Evaluator  
> **Goal:** AI-powered system to analyze GitHub profiles and provide actionable job-readiness insights  
> **Target Roles:** Software Engineering / AI / ML  
> **Document Version:** 1.0  
> **Last Updated:** April 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Core Functionality](#2-core-functionality)
3. [Scoring Framework](#3-scoring-framework)
4. [Feedback System](#4-feedback-system)
5. [Advanced Features](#5-advanced-features)
6. [System Architecture](#6-system-architecture)
7. [AI / LLM Integration](#7-ai--llm-integration)
8. [Tech Stack](#8-tech-stack)
9. [Database Design](#9-database-design)
10. [API Design](#10-api-design)
11. [Prompt Engineering](#11-prompt-engineering)
12. [MVP → Advanced Roadmap](#12-mvp--advanced-roadmap)
13. [Sample Evaluation Output](#13-sample-evaluation-output)
14. [Challenges & Solutions](#14-challenges--solutions)
15. [Deployment Strategy](#15-deployment-strategy)
16. [Cost Estimation](#16-cost-estimation)

---

## 1. System Overview

The GitHub Project Evaluator is a full-stack AI system that:

- Accepts a GitHub profile URL or username
- Fetches all public repositories via the GitHub REST API
- Analyzes each project deeply using LLMs + heuristics
- Produces a scored, ranked portfolio report
- Generates personalized, actionable feedback
- Simulates a recruiter's shortlisting decision
- Suggests what to build next to maximize hiring potential

### High-Level Data Flow

```
User Input (GitHub URL)
        │
        ▼
GitHub OAuth Authentication
        │
        ▼
GitHub Ingestion Service  ──►  Redis Cache (TTL: 1h)
        │
        ▼
Heuristic Pre-Scoring (fast, cheap)
        │
        ▼
Claude API Analysis Pipeline (per repo)
        │
        ├──► Code Quality Score
        ├──► Impact Score
        ├──► Innovation Score
        ├──► Completeness Score
        └──► Industry Relevance Score
                │
                ▼
        Aggregate Profile Score (0–100)
                │
                ▼
        Feedback Generation
        ├──► Improvement Suggestions
        ├──► Resume Bullet Points
        ├──► Recruiter Simulation
        ├──► AI Project Builder
        └──► AI-Rewritten README
                │
                ▼
        Dashboard (Next.js Frontend)
```

---

## 2. Core Functionality

### 2.1 GitHub Profile Ingestion

For each public repository, the system fetches:

| Data Point | GitHub API Endpoint | Notes |
|---|---|---|
| Repo metadata | `GET /repos/{owner}/{repo}` | Name, description, stars, forks, language, topics |
| File tree | `GET /repos/{owner}/{repo}/git/trees/HEAD?recursive=1` | Top-level structure only for large repos |
| README content | `GET /repos/{owner}/{repo}/readme` | Base64 decoded |
| Commit history | `GET /repos/{owner}/{repo}/commits?per_page=30` | Last 30 commits |
| Languages | `GET /repos/{owner}/{repo}/languages` | Byte breakdown |
| Releases | `GET /repos/{owner}/{repo}/releases` | Signals deployment maturity |
| Workflows | `GET /repos/{owner}/{repo}/actions/workflows` | CI/CD presence |

**Ingestion Strategy for Large Repos:**
- Never fetch the full file tree recursively for repos > 500 files
- Use tree API at depth 1, then selectively drill into: `/tests`, `/src`, `/app`, config files
- Sample commit messages from last 30 commits only
- Cap README analysis at 4,000 tokens

### 2.2 Analysis Dimensions

Each repository is analyzed across 7 dimensions:

| Dimension | Method | Weight |
|---|---|---|
| Code Quality | Claude API (rubric prompt) | 20 pts |
| Tech Stack Relevance | Embedding similarity vs demand index | 20 pts |
| Project Complexity | Claude API (classifier) | Categorical |
| Real-World Usefulness | Claude API (rubric prompt) | 20 pts |
| Documentation Quality | Heuristic + Claude API | 20 pts |
| Commit Consistency | Heuristic (time series analysis) | Bonus |
| Testing & Deployment | Heuristic (file tree scan) | 20 pts |

### 2.3 Complexity Classification

Each project is classified into one of three tiers:

- **Beginner:** CRUD apps, static sites, tutorial follow-alongs, single-file scripts
- **Intermediate:** APIs with auth, frontend + backend integration, database usage, third-party integrations
- **Advanced:** Distributed systems, ML pipelines, real-time data, novel algorithms, production deployments with monitoring

Classification is done by Claude with a few-shot prompt containing 3 examples per tier.

---

## 3. Scoring Framework

### 3.1 Per-Dimension Scoring (each out of 20)

#### Code Quality (20 pts)
Claude reviews:
- Folder structure and separation of concerns (+5)
- Naming conventions (functions, variables, files) (+4)
- Modularity (no monolithic files > 300 lines) (+4)
- Presence of configuration/environment files (+3)
- Error handling patterns (+4)

#### Impact & Usefulness (20 pts)
- Stars > 10: +4, Stars > 50: +8 (max +8)
- Live deployment URL found in README: +6
- Forks > 5: +3
- Claude rates real-world problem addressed: +3

#### Innovation (20 pts)
Claude compares idea against a "commodity project" list:
- Not a todo app / calculator / weather app: +8
- Novel tech combination or domain: +7
- Evidence of original research or unique approach: +5

Commodity project penalty: −10 pts automatically

#### Completeness (20 pts)
Heuristic checklist:
- README present: +4
- README has Setup / Installation section: +3
- Requirements / dependencies listed: +3
- Tests directory found: +4
- CI/CD config found (`.github/workflows`, `.travis.yml`, etc.): +3
- License file present: +2
- Demo link or screenshot in README: +1

#### Industry Relevance (20 pts)
Tech stack matched against demand index (updated monthly):

| Stack | Score |
|---|---|
| Python + ML (PyTorch, HuggingFace, scikit-learn) | 20 |
| TypeScript + React/Next.js | 18 |
| Rust, Go (systems/backend) | 17 |
| Python + FastAPI/Django | 16 |
| Java/Spring, Kotlin | 14 |
| PHP, jQuery, vanilla JS | 8 |
| Unknown / no clear stack | 5 |

### 3.2 Overall Profile Score

```
Per-Repo Score = (Code Quality + Impact + Innovation + Completeness + Relevance) / 5

Recency Weight:
  - Repos updated < 6 months ago: 1.5×
  - Repos updated 6–18 months ago: 1.0×
  - Repos updated > 18 months ago: 0.6×

Profile Score = weighted_mean(all repo scores) × consistency_bonus

Consistency Bonus:
  - Commits in ≥ 10 of last 12 months: +5 pts
  - Commits in ≥ 6 of last 12 months: +2 pts
  - Sporadic activity: 0

Max Profile Score: 100
```

### 3.3 Grade Scale

| Score | Grade | Label |
|---|---|---|
| 90–100 | A+ | Exceptional — Top 5% |
| 80–89 | A | Strong — Ready to interview |
| 70–79 | B+ | Good — Minor gaps |
| 60–69 | B | Developing — Clear roadmap needed |
| 50–59 | C | Early stage — Significant work needed |
| < 50 | D | Rebuild recommended |

---

## 4. Feedback System

### 4.1 Improvement Suggestions

Generated by Claude per-project. Prompt instructs model to output 3–5 bullets ranked by score ROI. Example output format:

```
1. [+17 pts] Add a /tests directory with at least 5 unit tests using pytest.
   This alone raises your Completeness score from 8 → 18.

2. [+9 pts] Deploy to Render or HuggingFace Spaces and add the live URL
   to your README. Impact score jumps from 11 → 20.

3. [+5 pts] Split app.py (currently 480 lines) into modules:
   routes.py, models.py, utils.py. Fixes your Code Quality deduction.
```

### 4.2 Missing Elements Detection

Severity classification:

| Issue | Severity | Score Impact |
|---|---|---|
| No README file | Critical | −12 pts |
| No tests | High | −8 pts |
| No deployment / live demo | High | −6 pts |
| No CI/CD | Medium | −4 pts |
| No license | Low | −2 pts |
| No project description | Low | −1 pt |

### 4.3 Resume-Level Feedback

Repos are ranked by "recruiter appeal" composite and labeled:

- **Feature on resume** — Top 3 repos by composite score; AI generates a STAR-format resume bullet for each
- **Mention in skills section** — Mid-tier repos; mentioned as supporting evidence only
- **Rebuild or archive** — Bottom-tier repos (score < 40) flagged for removal or major overhaul

### 4.4 Weak-to-Strong Conversion

For each "Rebuild" flagged repo, Claude produces:

```
Repo: todo-app (Score: 31)
This is a commodity project with no deployment and no tests.

3-Step Transformation Plan:
Step 1: Add collaborative real-time editing (WebSocket) → shifts from
        "basic CRUD" to "real-time systems" in recruiter's eye
Step 2: Deploy on Vercel + add Playwright e2e tests → raises
        Completeness from 10 → 18
Step 3: Add AI-powered task prioritization via Claude API → shifts
        Innovation score from 6 → 17

Estimated score after transformation: 31 → 79 (+48 pts)
Time investment: ~8 hours
```

---

## 5. Advanced Features

### 5.1 Recruiter View Mode

Simulates a senior hiring manager's 30-second profile scan.

**Prompt approach:** Claude is given a persona (e.g., "Senior Engineering Manager at a Series-B AI startup") and the full profile summary. It outputs:

```json
{
  "verdict": "Shortlist",
  "confidence": "Medium",
  "reasoning": "Strong ML project shows production thinking. Portfolio site has
                no live deployment and no tests, raising concerns about shipping
                discipline. One more production-grade project would push to
                Strong Hire.",
  "single_biggest_fix": "Deploy ml-fraud-detector with a live API endpoint and
                          add a demo GIF to the README.",
  "would_reach_out": true
}
```

**Three verdict levels:**
- Strong Hire — would fast-track to technical screen
- Shortlist — would review further, not immediate pass
- Reject — would not proceed; specific blocking reason given

### 5.2 Growth Tracker

- Every analysis run stores a score snapshot in PostgreSQL with timestamp
- Frontend renders sparkline chart of overall score over time
- Weekly cron job (Celery beat) re-analyzes all active user profiles
- Email notification sent when score changes by ± 5 points or more
- Monthly summary email: "Your GitHub improved by +23 points this month — here's why"

### 5.3 AI Project Builder

Uses skill-gap analysis to generate concrete project briefs:

```
Detected gaps in your profile:
  ✗ No streaming / real-time systems project
  ✗ No API design (all projects are scripts or frontends)
  ✗ No cloud deployment (AWS/GCP/Azure)

Recommended Build:
  Title: Real-Time Fraud Detection API
  Stack: Python + FastAPI + Kafka + PostgreSQL + React dashboard
  Complexity: Advanced
  Deploy: AWS ECS (free tier) + RDS
  Estimated build time: 3–4 weekends
  Estimated profile score boost: +22 points
  Fills gaps: streaming systems, API design, cloud deployment
  
  Architecture sketch:
    Transaction events → Kafka → FastAPI consumer → ML model inference
    → PostgreSQL (results) → React dashboard (live updates via WebSocket)
```

"Profile score boost" is calculated from the scoring model's feature importances — the system knows exactly which gap is costing the most points.

### 5.4 Resume Sync

Generates STAR-format resume bullets from repo data:

**Input:** Repo metadata, commit history, star/fork counts, tech stack, deployment info

**Output:**
```
ml-fraud-detector:
• Built a real-time fraud detection system using Python, FastAPI, and
  scikit-learn that processes 10K+ transactions/sec; deployed on AWS
  ECS with 99.9% uptime; achieved 94.2% detection accuracy on held-out
  test set.

• Reduced false positive rate by 31% vs baseline logistic regression
  by implementing an ensemble of gradient boosting + isolation forest;
  project received 47 GitHub stars.
```

Output formats: Plain text, JSON (for programmatic use), downloadable PDF.

### 5.5 Comparison Engine

- User's tech-stack list is embedded using text-embedding-3-small
- Compared via cosine similarity to curated index of top GitHub profiles per role
- Radar chart shows gap across: ML/AI, Backend, Frontend, DevOps, Open Source contributions, Documentation
- Outputs: "You are in the 62nd percentile for ML engineers. Your biggest gap vs top profiles: no open source contributions and no cloud infrastructure projects."

---

## 6. System Architecture

### 6.1 Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│                    Browser / Mobile                         │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS
┌─────────────────────────▼───────────────────────────────────┐
│                    FRONTEND LAYER                           │
│   Next.js 14 (App Router) + TypeScript + TailwindCSS        │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│   │Dashboard │ │  Repo    │ │Recruiter │ │   Growth     │  │
│   │(overview)│ │Analysis  │ │  View    │ │   Tracker    │  │
│   └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST + WebSocket
┌─────────────────────────▼───────────────────────────────────┐
│                    API GATEWAY LAYER                        │
│              FastAPI + OAuth2 + Rate Limiting               │
└──────┬──────────┬──────────┬────────────┬───────────────────┘
       │          │          │            │
┌──────▼──┐ ┌────▼────┐ ┌───▼─────┐ ┌───▼──────────┐
│ GitHub  │ │Scoring  │ │   AI    │ │    Resume    │
│Ingestion│ │ Engine  │ │Orchestr.│ │     Sync     │
└──────┬──┘ └────┬────┘ └───┬─────┘ └───┬──────────┘
       │          │          │            │
┌──────▼──────────▼──────────▼────────────▼──────────┐
│                    AI / LLM LAYER                  │
│  ┌──────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐ │
│  │  Claude  │ │Embedding │ │  Rec  │ │ Skill Gap│ │
│  │   API    │ │+ Ranking │ │Engine │ │    AI    │ │
│  └──────────┘ └──────────┘ └───────┘ └──────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │    Prompt Pipeline: Analyze→Score→Suggest→Gen  │ │
│  └────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────┐
│                   DATA LAYER                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │PostgreSQL│  │  Redis   │  │  S3/Object Store │ │
│  │users     │  │  Cache   │  │  READMEs, PDFs   │ │
│  │repos     │  │(TTL: 1h) │  │  resume exports  │ │
│  │scores    │  │          │  │                  │ │
│  │snapshots │  │          │  │                  │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
└────────────────────────┬───────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────┐
│              EXTERNAL INTEGRATIONS                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  GitHub  │  │Anthropic │  │  Celery +        │ │
│  │ REST API │  │   API    │  │  RabbitMQ        │ │
│  │(OAuth)   │  │(Claude)  │  │  (async jobs)    │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────┘
```

### 6.2 Key Design Decisions

- **Async-first:** All GitHub API calls and LLM calls are non-blocking. Users see partial results within 3 seconds while background workers complete the analysis.
- **Cache-heavy:** Redis caches GitHub API responses (1h TTL) and LLM analysis results (24h TTL). Repeat visits are instant.
- **Job queue:** Celery + RabbitMQ handles background analysis. This decouples the API response time from the actual analysis duration.
- **Structured LLM output:** All Claude API calls request JSON output via tool-use. No regex parsing of free text.

---

## 7. AI / LLM Integration

### 7.1 Where LLMs Are Used

| Task | Model | Approx Cost/Run |
|---|---|---|
| Deep repo analysis (code quality, innovation) | claude-sonnet-4 | ~$0.04/repo |
| README generation | claude-sonnet-4 | ~$0.03/repo |
| Recruiter simulation | claude-sonnet-4 | ~$0.02/profile |
| Resume bullet generation | claude-haiku-4 | ~$0.003/repo |
| Complexity classification | claude-haiku-4 | ~$0.001/repo |
| Quick completeness check | Heuristic (no LLM) | $0 |
| Tech stack embedding | text-embedding-3-small | ~$0.0001/repo |

### 7.2 Prompt Pipeline

Analysis runs in 4 sequential steps per repository:

**Step 1 — Analyze** (claude-sonnet-4)
```
Input: file tree, README, commit messages, stars, forks, language, topics
Output: JSON scores for all 5 dimensions + brief reasoning per dimension
```

**Step 2 — Score** (deterministic, no LLM)
```
Input: JSON scores from Step 1 + heuristic checklist results
Output: weighted composite score
```

**Step 3 — Suggest** (claude-sonnet-4)
```
Input: scores + identified gaps
Output: 3–5 improvement actions ranked by score ROI
```

**Step 4 — Generate** (claude-haiku-4 or claude-sonnet-4 depending on task)
```
Input: repo metadata + scores
Output: resume bullet, README draft, LinkedIn description
```

### 7.3 Core Analysis Prompt

```
System:
You are a senior software engineering hiring manager and code reviewer
with 10+ years of experience evaluating developer portfolios at top tech
companies. You evaluate GitHub repositories objectively and provide
scores as structured JSON.

User:
Analyze this GitHub repository and return scores matching the schema.

Repository: {repo_name}
Primary Language: {language}
Description: {description}
Topics: {topics}
Stars: {stars} | Forks: {forks} | Watchers: {watchers}

File Structure (top 40 files):
{file_tree}

README Content:
{readme_content}

Recent Commit Messages (last 30):
{commit_log}

CI/CD Files Found: {ci_files}
Test Directories Found: {test_dirs}
Deployment Indicators: {deploy_indicators}

Return ONLY valid JSON matching this schema:
{
  "code_quality": {
    "score": <0-20>,
    "top_issue": "<15 words max>",
    "improvement": "<20 words max>"
  },
  "impact": {
    "score": <0-20>,
    "top_issue": "<15 words max>",
    "improvement": "<20 words max>"
  },
  "innovation": {
    "score": <0-20>,
    "is_commodity_project": <true|false>,
    "top_issue": "<15 words max>",
    "improvement": "<20 words max>"
  },
  "industry_relevance": {
    "score": <0-20>,
    "detected_stack": ["<tech1>", "<tech2>"],
    "top_issue": "<15 words max>",
    "improvement": "<20 words max>"
  },
  "complexity_tier": "<beginner|intermediate|advanced>",
  "resume_worthy": <true|false>,
  "one_line_summary": "<20 words max>"
}
```

### 7.4 Recruiter Simulation Prompt

```
System:
You are a {target_role} hiring manager at a {company_tier} company.
You have 30 seconds to scan a developer's GitHub profile.
Be direct, realistic, and slightly critical — you see hundreds of profiles.

User:
Profile summary:
  Username: {username}
  Overall score: {score}/100
  Top repos: {top_repos_summary}
  Tech stack: {detected_stacks}
  Activity: {activity_summary}
  Strengths: {strengths}
  Weaknesses: {weaknesses}

Return JSON:
{
  "verdict": "<Strong Hire|Shortlist|Reject>",
  "confidence": "<High|Medium|Low>",
  "reasoning": "<2 sentences, direct tone>",
  "biggest_blocker": "<1 sentence if Reject or Shortlist>",
  "single_biggest_fix": "<1 actionable sentence>",
  "would_reach_out": <true|false>
}
```

---

## 8. Tech Stack

### 8.1 Recommended Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript | SSR for SEO, App Router for streaming, TS for safety |
| Styling | TailwindCSS | Rapid UI, consistent design system |
| Charts | Recharts | Lightweight, React-native, good defaults |
| Backend | FastAPI (Python 3.11+) | Best LLM SDK ecosystem, async-native, fast |
| Task Queue | Celery + RabbitMQ | Battle-tested async job processing |
| Primary DB | PostgreSQL 15 | ACID, JSON columns for flexible schema |
| Cache | Redis 7 | TTL-based caching, rate-limit state |
| Object Store | S3 (or MinIO for local dev) | Generated artifacts, PDF exports |
| AI Analysis | Anthropic Claude API (claude-sonnet-4) | Best reasoning, structured JSON output |
| AI Fast Tasks | Anthropic Claude API (claude-haiku-4) | 10× cheaper for classification tasks |
| Embeddings | OpenAI text-embedding-3-small | Cost-effective, 1536-dim |
| Vector Search | pgvector (PostgreSQL extension) | No extra infra needed for MVP |
| Auth | GitHub OAuth 2.0 | Natural fit; provides GitHub token for API access |
| Email | Resend | Simple API, reliable delivery |
| Deployment | Railway (MVP) → AWS ECS (scale) | Zero DevOps for MVP, scalable later |
| Monitoring | Sentry + Prometheus + Grafana | Error tracking + metrics |

### 8.2 Local Development Setup

```bash
# Prerequisites
node >= 20, python >= 3.11, docker, docker-compose

# Clone and setup
git clone https://github.com/your-org/github-evaluator
cd github-evaluator

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add API keys

# Frontend
cd ../frontend
npm install
cp .env.local.example .env.local

# Start all services
docker-compose up -d  # PostgreSQL, Redis, RabbitMQ

# Run services
cd backend && uvicorn main:app --reload
cd backend && celery -A worker worker --loglevel=info
cd frontend && npm run dev
```

---

## 9. Database Design

### 9.1 PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  github_id     INTEGER UNIQUE NOT NULL,
  username      VARCHAR(100) NOT NULL,
  email         VARCHAR(255),
  access_token  TEXT,  -- encrypted GitHub OAuth token
  plan          VARCHAR(20) DEFAULT 'free',  -- free | pro
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  last_analyzed TIMESTAMPTZ
);

-- Repositories table
CREATE TABLE repositories (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
  github_id     INTEGER NOT NULL,
  name          VARCHAR(255) NOT NULL,
  full_name     VARCHAR(255) NOT NULL,
  description   TEXT,
  language      VARCHAR(100),
  topics        TEXT[],
  stars         INTEGER DEFAULT 0,
  forks         INTEGER DEFAULT 0,
  is_fork       BOOLEAN DEFAULT FALSE,
  created_at    TIMESTAMPTZ,
  updated_at    TIMESTAMPTZ,
  pushed_at     TIMESTAMPTZ,
  raw_data      JSONB,  -- full GitHub API response
  fetched_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Analysis results table
CREATE TABLE analyses (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  repo_id               UUID REFERENCES repositories(id) ON DELETE CASCADE,
  user_id               UUID REFERENCES users(id) ON DELETE CASCADE,
  code_quality_score    SMALLINT CHECK (code_quality_score BETWEEN 0 AND 20),
  impact_score          SMALLINT CHECK (impact_score BETWEEN 0 AND 20),
  innovation_score      SMALLINT CHECK (innovation_score BETWEEN 0 AND 20),
  completeness_score    SMALLINT CHECK (completeness_score BETWEEN 0 AND 20),
  relevance_score       SMALLINT CHECK (relevance_score BETWEEN 0 AND 20),
  composite_score       NUMERIC(5,2),
  complexity_tier       VARCHAR(20),  -- beginner | intermediate | advanced
  is_commodity_project  BOOLEAN DEFAULT FALSE,
  resume_worthy         BOOLEAN,
  one_line_summary      TEXT,
  ai_reasoning          JSONB,  -- full per-dimension reasoning from Claude
  improvement_actions   JSONB,  -- ranked list of suggestions
  resume_bullet         TEXT,
  generated_readme      TEXT,
  linkedin_description  TEXT,
  model_used            VARCHAR(100),
  tokens_used           INTEGER,
  analyzed_at           TIMESTAMPTZ DEFAULT NOW()
);

-- Profile score snapshots (for Growth Tracker)
CREATE TABLE profile_snapshots (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  overall_score   NUMERIC(5,2),
  grade           VARCHAR(5),
  repos_analyzed  INTEGER,
  recruiter_verdict VARCHAR(20),
  snapshot_data   JSONB,  -- full profile summary at point in time
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Recruiter simulations
CREATE TABLE recruiter_simulations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  target_role     VARCHAR(100),
  company_tier    VARCHAR(50),
  verdict         VARCHAR(20),
  confidence      VARCHAR(10),
  reasoning       TEXT,
  biggest_fix     TEXT,
  would_reach_out BOOLEAN,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Project recommendations (AI Project Builder)
CREATE TABLE project_recommendations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  title           VARCHAR(255),
  description     TEXT,
  tech_stack      TEXT[],
  complexity_tier VARCHAR(20),
  score_boost_est NUMERIC(4,1),
  gaps_filled     TEXT[],
  build_hours_est INTEGER,
  is_dismissed    BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_repos_user_id ON repositories(user_id);
CREATE INDEX idx_analyses_repo_id ON analyses(repo_id);
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_snapshots_user_id_created ON profile_snapshots(user_id, created_at DESC);
```

### 9.2 Redis Key Structure

```
# GitHub API response cache
github:repos:{username}          → JSON array of repos     TTL: 1h
github:readme:{owner}:{repo}     → README content          TTL: 1h
github:commits:{owner}:{repo}    → commit array            TTL: 1h

# Analysis cache
analysis:{repo_id}               → analysis JSON           TTL: 24h
profile:{user_id}:summary        → profile summary JSON    TTL: 1h

# Rate limit tracking
ratelimit:github:{user_id}       → request count           TTL: 1h
ratelimit:claude:{user_id}       → request count           TTL: 1h

# Job status
job:{job_id}:status              → pending|running|done    TTL: 24h
job:{job_id}:progress            → integer 0-100           TTL: 24h
```

---

## 10. API Design

### 10.1 REST Endpoints

```
Authentication
  GET  /auth/github              → Initiate GitHub OAuth
  GET  /auth/callback            → OAuth callback, return JWT
  POST /auth/logout              → Invalidate session

Profile Analysis
  POST /analyze                  → Trigger full profile analysis
       Body: { "username": "priya-sharma" }
       Returns: { "job_id": "uuid", "status": "queued" }

  GET  /profile/{username}       → Fetch cached analysis results
  GET  /profile/{username}/repos → Fetch individual repo scores
  GET  /profile/{username}/history → Growth tracker data

Job Status
  GET  /jobs/{job_id}            → Poll analysis job status + progress
       Returns: { "status": "running", "progress": 60, "partial_results": [...] }

AI Features
  POST /generate/readme          → Generate improved README for a repo
       Body: { "repo_id": "uuid" }

  POST /generate/resume          → Generate resume bullets for top repos
       Body: { "user_id": "uuid", "format": "pdf|json|text" }

  GET  /recruiter-view/{username} → Run recruiter simulation
       Query: ?role=ml-engineer&tier=faang

  GET  /recommendations/{username} → AI project builder suggestions

Comparison
  GET  /compare/{username}       → Compare vs top profiles in target role
       Query: ?role=ml-engineer

Admin / Internal
  POST /internal/cron/refresh    → Triggered by Celery beat weekly
```

### 10.2 WebSocket

```
ws://api/ws/analysis/{job_id}

Server pushes events:
  { "type": "progress", "value": 45, "current_repo": "ml-fraud-detector" }
  { "type": "repo_done", "repo": "ml-fraud-detector", "score": 84 }
  { "type": "complete", "profile_score": 72, "grade": "B+" }
  { "type": "error", "message": "GitHub API rate limit hit, retrying in 30s" }
```

---

## 11. Prompt Engineering

### 11.1 Prompt Design Principles

- Always request JSON output via Claude's tool-use API (not free text)
- Include explicit field constraints (word limits, value ranges) in the schema
- Use few-shot examples for classification tasks (complexity tier)
- Separate system persona from user data clearly
- Version all prompts (store in DB, reference by hash in analysis record)

### 11.2 Prompt Versioning Strategy

All prompts are stored in `prompts/` directory and referenced by SHA hash in each analysis record. This allows:
- A/B testing different prompt versions
- Auditing what prompt produced a given score
- Rolling back if a prompt change degrades quality

### 11.3 Token Budget per Repo Analysis

| Input Component | Max Tokens |
|---|---|
| System prompt | 400 |
| Repo metadata | 200 |
| File tree | 600 |
| README | 1,500 |
| Commit messages | 400 |
| Buffer | 100 |
| **Total input** | **~3,200** |
| **Output (JSON)** | **~600** |
| **Total per repo** | **~3,800 tokens** |

At claude-sonnet-4 pricing (~$3/1M input, ~$15/1M output):
- Cost per repo: ~$0.009 input + $0.009 output = ~$0.018
- 20-repo profile: ~$0.36 per full analysis run

---

## 12. MVP → Advanced Roadmap

### Phase 0: Foundation (Weeks 1–2)

**Goal:** Core infrastructure, no AI yet.

- [ ] Set up monorepo (Next.js frontend + FastAPI backend)
- [ ] GitHub OAuth integration
- [ ] GitHub API ingestion service (fetch repos, READMEs, commits)
- [ ] PostgreSQL schema + migrations (Alembic)
- [ ] Redis setup + caching layer
- [ ] Basic heuristic scoring (completeness checklist only, no LLM)
- [ ] Simple dashboard showing repos with heuristic scores
- [ ] Docker Compose for local dev

**Deliverable:** User can log in with GitHub, see their repos listed with basic completeness scores.

---

### Phase 1: MVP — AI Core (Weeks 3–6)

**Goal:** Working AI analysis pipeline, shareable results.

- [ ] Integrate Claude API for deep repo analysis
- [ ] Implement all 5 scoring dimensions
- [ ] Celery + RabbitMQ for async analysis jobs
- [ ] WebSocket for live progress updates in frontend
- [ ] Per-repo feedback and improvement suggestions
- [ ] Overall profile score with grade
- [ ] Recruiter View Mode (basic version)
- [ ] Shareable profile report link (public, no auth required)

**Deliverable:** Users can analyze their GitHub profile end-to-end and share results.

---

### Phase 2: V1 — Feedback & Generation (Weeks 7–10)

**Goal:** Full feedback suite, resume tools.

- [ ] AI-generated improved README per repo
- [ ] Resume bullet generator (STAR format)
- [ ] PDF export of full report + resume bullets
- [ ] Weak-to-strong conversion plans
- [ ] Completeness checklist UI with actionable links
- [ ] Missing elements detection with severity badges
- [ ] Recruiter View: full persona selection (role + company tier)
- [ ] Growth Tracker (score history sparklines)
- [ ] Weekly email digest (Resend integration)

**Deliverable:** Paid feature tier justified; production-ready for beta launch.

---

### Phase 3: V2 — Intelligence & Comparison (Weeks 11–16)

**Goal:** Differentiated features that justify premium pricing.

- [ ] Skill Gap Analysis with visual radar chart
- [ ] Comparison Engine vs top profiles (pgvector embeddings)
- [ ] AI Project Builder with score boost estimates
- [ ] LinkedIn auto-description generator
- [ ] Commodity project detector (penalizes todo apps etc.)
- [ ] Industry demand index (monthly updated tech stack rankings)
- [ ] Batch analysis for organizations/teams
- [ ] API access tier for power users

**Deliverable:** Full product feature set; ready for public launch and paid tiers.

---

### Phase 4: Advanced — Scale & Moat (Weeks 17+)

**Goal:** Defensible data moat and enterprise features.

- [ ] GitHub Action: auto-analyze on every push, post score badge to PR
- [ ] VS Code extension: inline score + suggestions while coding
- [ ] Interview readiness score (projects mapped to common interview topics)
- [ ] Company-specific analysis ("Optimize profile for Google ML roles")
- [ ] Cohort benchmarking (compare against bootcamp cohort, university peers)
- [ ] White-label for coding bootcamps and universities
- [ ] Enterprise dashboard for hiring teams to screen candidates at scale

---

## 13. Sample Evaluation Output

### Profile: `github.com/priya-sharma-dev`

```
Overall GitHub Score: 67 / 100   Grade: B   "Good foundation, needs polish"
Profile analyzed: 8 repositories | Active months (last 12): 9 of 12
```

#### Repository Breakdown

| Repo | Code | Impact | Innovation | Complete | Relevance | Total | Tier | Verdict |
|---|---|---|---|---|---|---|---|---|
| ml-fraud-detector | 17 | 14 | 18 | 12 | 20 | **84** | Advanced | ⭐ Feature |
| python-scraper | 14 | 10 | 13 | 14 | 16 | **71** | Intermediate | ✓ Mention |
| fastapi-blog-api | 13 | 8 | 10 | 15 | 16 | **68** | Intermediate | ✓ Mention |
| react-portfolio | 10 | 6 | 8 | 10 | 14 | **52** | Beginner | ⚠ Rebuild |
| todo-app | 7 | 2 | 2 | 8 | 10 | **31** | Beginner | ✗ Archive |

#### Recruiter Simulation (Target: ML Engineer @ Series-B startup)

```
Verdict:      SHORTLIST
Confidence:   Medium
Reasoning:    "ml-fraud-detector shows real-world ML thinking and is nearly
               interview-ready. The portfolio is dragged down by commodity
               projects (todo-app) and missing deployment on the blog API.
               One more production-grade deployed project = Strong Hire."
Biggest fix:  "Deploy fastapi-blog-api on Render, add /tests, and push to
               production — this alone could shift you to Strong Hire."
Would reach out: YES
```

#### Top Action Items (Ranked by Score ROI)

```
1. [+19 pts] Add pytest tests to ml-fraud-detector and deploy a live
   API endpoint (Render free tier). Score: 84 → 97.

2. [+14 pts] Add CI/CD (GitHub Actions) and a deployment to fastapi-blog-api.
   Score: 68 → 82.

3. [+8 pts]  Archive todo-app. Its presence actively hurts profile perception.
   Removing it raises weighted average by 8 points.

4. [+6 pts]  Add a demo GIF or screenshot to ml-fraud-detector README.
   Takes 20 minutes; significantly increases recruiter dwell time.
```

#### AI Project Builder — Top Recommendation

```
Build: Real-Time Anomaly Detection Dashboard
Stack: FastAPI + WebSocket + Kafka + React + PostgreSQL
Deploy: AWS ECS (free tier) + RDS
Est. build time: 3 weekends
Score boost: +22 points
Fills gaps: streaming systems, full-stack integration, cloud deployment
```

#### Resume Bullets (Auto-Generated)

```
ml-fraud-detector:
• Designed and deployed a real-time financial fraud detection system
  using Python, scikit-learn, and FastAPI; achieved 94.2% accuracy on
  held-out test set using an ensemble of gradient boosting + isolation
  forest; system processes 10K+ events/sec.
```

---

## 14. Challenges & Solutions

### 14.1 GitHub API Rate Limits

**Problem:** Authenticated users get 5,000 requests/hour. A 30-repo profile with commits, READMEs, and file trees can consume 90–150 requests.

**Solutions:**
- Cache all raw API responses in Redis (1h TTL) — repeat analyses are free
- Use GitHub GraphQL API for batch fetching (1 query = multiple REST calls)
- Implement exponential backoff with jitter on 429 responses
- Show partial results as repos complete — don't block UI on full completion
- For unauthenticated users, limit to 5 repos and prompt for OAuth

### 14.2 Large Repositories

**Problem:** Repos with 1,000+ files cause token overflow and slow analysis.

**Solutions:**
- Cap file tree at depth 2 (top-level + one level deep)
- Selectively fetch only quality-signal files: `tests/`, `src/`, `app/`, CI configs, package files
- Cap README at 4,000 tokens; truncate with note to Claude
- Skip binary files, images, and lock files from tree listing

### 14.3 LLM Accuracy & Hallucination

**Problem:** Claude may invent test files that don't exist, or misread code style from a file listing.

**Solutions:**
- Ground all scoring in structured inputs (actual file paths, actual commit messages)
- Never ask Claude to assume what's inside files it hasn't seen
- Apply heuristic bounds: Claude can't give 18/20 to a repo with 0 commits or no README
- Validate JSON output against schema; retry with error feedback if schema fails
- Log token inputs + outputs for every analysis for auditability

### 14.4 LLM Cost at Scale

**Problem:** 1,000 users × 20 repos × $0.018/repo = $360/day at scale.

**Solutions:**
- Use claude-haiku-4 for classification tasks (10× cheaper)
- Only escalate to claude-sonnet-4 for repos scoring above threshold in haiku pass
- Cache analysis results for 24h — re-analysis only on user request or weekly cron
- Introduce usage limits on free tier (5 repos/day) to control costs
- Batch multiple repo analyses in a single Claude API call where possible

### 14.5 Scoring Subjectivity

**Problem:** Two evaluators might score the same repo differently. LLM outputs may vary between runs.

**Solutions:**
- Use temperature=0 for all scoring calls (deterministic output)
- Anchor with few-shot examples in system prompt
- Heuristic floor: if checklist score is 0 (no README, no tests), AI score is capped at 40
- Store the exact prompt + model version in each analysis record for reproducibility

### 14.6 Profile Freshness

**Problem:** User updates their GitHub but sees stale scores.

**Solutions:**
- Store `last_analyzed_at` timestamp, show "Analyzed 3 days ago — Re-analyze" button
- Weekly cron (Celery beat) re-analyzes profiles of users active in last 30 days
- Webhook listener for GitHub push events (GitHub App integration) for real-time updates
- Score change notifications via email when delta > 5 points

---

## 15. Deployment Strategy

### 15.1 MVP Deployment (Railway)

```yaml
# railway.toml
[build]
  builder = "dockerfile"

[services.api]
  dockerfile = "backend/Dockerfile"
  envVars:
    - DATABASE_URL
    - REDIS_URL
    - ANTHROPIC_API_KEY
    - GITHUB_CLIENT_ID
    - GITHUB_CLIENT_SECRET

[services.worker]
  dockerfile = "backend/Dockerfile.worker"

[services.frontend]
  dockerfile = "frontend/Dockerfile"
```

Railway provides: PostgreSQL, Redis, managed deployments, auto-scaling, and a free tier. Zero infrastructure management for MVP.

### 15.2 Production Deployment (AWS)

```
Route 53 (DNS)
    │
CloudFront CDN
    │
ALB (Application Load Balancer)
    ├──► ECS Fargate (FastAPI containers) — auto-scales 1–10 tasks
    └──► ECS Fargate (Celery workers) — auto-scales 1–20 tasks

RDS PostgreSQL (Multi-AZ)
ElastiCache Redis (Cluster mode)
S3 (artifacts)
SQS (job queue — replaces RabbitMQ for serverless scale)
SES (email — replaces Resend at volume)
```

### 15.3 Environment Variables

```bash
# Required
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
JWT_SECRET=...

# Optional
OPENAI_API_KEY=...         # For embeddings
RESEND_API_KEY=...         # For email
SENTRY_DSN=...             # For error tracking
S3_BUCKET=...              # For artifact storage
S3_REGION=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

---

## 16. Cost Estimation

### 16.1 MVP Stage (0–500 users/month)

| Service | Cost/Month |
|---|---|
| Railway (API + Worker + DB + Redis) | ~$25 |
| Anthropic API (avg 10 analyses/day × $0.40) | ~$120 |
| GitHub API | Free (OAuth) |
| Resend (email) | Free tier |
| Domain + SSL | ~$15/year |
| **Total MVP** | **~$150/month** |

### 16.2 Growth Stage (5,000 users/month)

| Service | Cost/Month |
|---|---|
| AWS ECS + RDS + ElastiCache | ~$200 |
| Anthropic API (100 analyses/day × $0.40) | ~$1,200 |
| OpenAI Embeddings | ~$20 |
| S3 + CloudFront | ~$30 |
| Resend (email) | ~$20 |
| Sentry | ~$26 |
| **Total Growth** | **~$1,500/month** |

Break-even at growth stage: ~150 Pro users at $10/month, or ~30 users at $49/month.

---

*End of Implementation Plan — GitHub Project Evaluator v1.0*

*This document should be treated as a living spec. Update it as architectural decisions evolve.*
