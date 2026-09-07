# Aakash AI - Personal Voice Bot

> *"Talk to an AI that answers as Aakash would."*

[![Vite](https://img.shields.io/badge/Frontend-Vite%20%2B%20React%20%2B%20TS-646CFF?logo=vite)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/AI%20Engine-Groq%20Llama%203.3%2070B-f55036)](https://groq.com/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC?logo=tailwindcss)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)](https://www.docker.com/)

**Aakash AI** is a production-quality, deployable conversational AI voice bot web application representing Aakash Kumar. Users can interact seamlessly via microphone voice recording or text fallback, receive personality-grounded first-person responses, and hear answers spoken aloud in a realistic Indian English male voice.

---

## 🌟 Key Features & Upgrades

1. **Zero Key Requirement for Evaluators**: Functions out-of-the-box using built-in intelligent fallback engines without requiring the evaluator to supply an API key or PostgreSQL database.
2. **Groq AI Engine Support**: Seamless 100% free AI integration via Groq API Key powering **Llama 3.3 70B** (`llama-3.3-70b-versatile`) for responses and **Whisper Large v3** (`whisper-large-v3`) for speech transcription.
3. **Realistic Neural TTS (Indian English Male Voice)**: Integrated Microsoft Edge Neural AI TTS (`en-IN-PrabhatNeural`) providing high-quality, human-like Indian English male voice output 100% free.
4. **Live Microphone Speech-to-Text**: Real-time browser Web Speech API integration combined with backend Whisper STT to ensure 100% transcript accuracy between spoken voice and AI response.
5. **Voice Cloning Support**: Plug-and-play provider abstraction for ElevenLabs (`ELEVENLABS_API_KEY` & `ELEVENLABS_VOICE_ID`) and OpenAI TTS (`tts-1` with male voices `echo`/`onyx`).
6. **Authentic Personality Grounding**: Answer generation grounded by Aakash's real background (IIT Kanpur B.Tech, JNU Master's, software developer background in FastAPI, React, Spring Boot, PostgreSQL, RAG, and LangGraph agentic frameworks).
7. **Dual-Mode Voice & Text Interface**: Touch-friendly animated microphone recording using `MediaRecorder` API alongside responsive text chat fallback.
8. **Multi-turn Context Memory**: Maintains history across follow-up questions for conversational continuity.
9. **Robust Safety & Fallbacks**: User-friendly toasts for microphone permissions, browser compatibility, and server connection failures without raw stack traces.

---

## 🏗️ Architecture Overview

```
 USER
  │
  ▼
React + Vite SPA (Vercel)
  │ (REST API / MediaRecorder / Web Speech API / HTML5 Audio)
  ▼
FastAPI Backend (Railway/Render)
  ├── POST /api/v1/voice/chat ──► Speech-to-Text (Groq Whisper v3 / OpenAI Whisper / Browser Transcript)
  ├── POST /api/v1/chat       ──► Intent Classifier & Personality Engine (Groq Llama 3.3 70B / OpenAI / Fallback)
  ├── POST /api/v1/tts        ──► Text-to-Speech (Edge Neural en-IN-PrabhatNeural / ElevenLabs / OpenAI TTS)
  ├── GET  /api/v1/health     ──► System Health Check
  └── Repositories            ──► SQLAlchemy PostgreSQL / In-Memory Store
```

---

## 📁 Project Structure

```
100xAakashVoiceBot/
├── PROJECT_PHASES.md          # Project development phases document
├── docker-compose.yml         # Container orchestration for FastAPI & Postgres
├── README.md                  # Detailed documentation
│
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI main app & middleware setup
│   │   ├── config.py          # Settings management with Pydantic (Groq, OpenAI, ElevenLabs)
│   │   ├── dependencies.py    # Dependency injection helpers
│   │   ├── api/               # REST API endpoints (health, chat, voice, conversations, tts)
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic layer (conversation, voice, STT, LLM)
│   │   ├── providers/         # Provider abstractions:
│   │   │   ├── llm/           # Groq Llama 3.3 70B, OpenAI GPT-4o-mini, Mock LLM
│   │   │   ├── speech/        # Groq Whisper v3, OpenAI Whisper, Mock STT
│   │   │   └── tts/           # Edge Neural TTS (en-IN-PrabhatNeural), ElevenLabs, OpenAI TTS
│   │   ├── personality/       # Profile data, golden answers, system prompt, classifier
│   │   ├── repositories/      # DB & In-Memory conversation repository
│   │   ├── db/                # SQLAlchemy models and async engine
│   │   └── core/              # Structured logging, middleware, security validators
│   ├── tests/                 # Pytest test suite (health, chat, voice, personality)
│   ├── Dockerfile             # Production container definition
│   ├── requirements.txt       # Python dependencies (fastapi, uvicorn, edge-tts, etc.)
│   └── .env                   # Environment variable configuration
│
└── frontend/
    ├── src/
    │   ├── components/        # VoiceBot, Header, Hero, MicrophoneButton, AudioVisualizer, etc.
    │   ├── hooks/             # useAudioRecorder, useSpeechSynthesis, useVoiceBot
    │   ├── services/          # Fetch API wrapper (health, chat, voice, tts)
    │   ├── types/             # TypeScript definitions
    │   ├── utils/             # Audio MIME detection & helpers
    │   ├── App.tsx            # Main application component
    │   ├── main.tsx           # React DOM entrypoint
    │   └── index.css          # Tailwind CSS directives & glassmorphic tokens
    ├── package.json           # Frontend dependencies
    ├── tsconfig.json          # TypeScript configuration
    ├── vite.config.ts         # Vite build configuration
    └── vercel.json            # Vercel SPA routing rewrite rules
```

---

## 🚀 Quick Local Setup

### 1. Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Git

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.venv\Scripts\activate.bat
# On Linux/macOS (Bash/Zsh):
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables in backend/.env
# Add your free Groq API key (optional):
# GROQ_API_KEY=gsk_your_groq_api_key_here

# Run FastAPI development server:
python -m uvicorn app.main:app --reload --port 8000
```
Backend will be available at `http://localhost:8000`. Health check endpoint: `http://localhost:8000/api/v1/health`.

### 3. Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run Vite dev server
npm run dev
```
Frontend application will be accessible at `http://localhost:5173`.

---

## 🔑 Environment Variables (`backend/.env`)

```env
APP_ENV=development
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

# 100% Free High-Speed AI Provider (Recommended)
LLM_PROVIDER=groq
STT_PROVIDER=groq
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_LLM_MODEL=llama-3.3-70b-versatile
GROQ_STT_MODEL=whisper-large-v3

# Optional: OpenAI API Settings
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Optional: ElevenLabs Voice Cloning
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=

# Optional: PostgreSQL Database (Defaults to In-Memory store if blank)
DATABASE_URL=
```

---

## 🐳 Running with Docker

Launch both the FastAPI backend and PostgreSQL database with Docker Compose:

```bash
# In the project root:
docker-compose up --build
```

---

## 🧪 Running Tests

Run the backend test suite without needing real API keys:

```bash
cd backend
python -m pytest -v
```

---

## 🌐 Deployment Configuration

### Frontend (Vercel)
1. Import `frontend/` repository into Vercel.
2. Set build command to `npm run build` and output directory to `dist`.
3. Set environment variable: `VITE_API_BASE_URL=https://your-backend-domain.up.railway.app/api/v1`.

### Backend (Railway / Render)
1. Deploy `backend/` using Dockerfile or Python buildpack.
2. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Set environment variables (`GROQ_API_KEY`, `CORS_ORIGINS`, etc.).

---

## 🎯 Sample Questions for Evaluators

- *"What should we know about your life story?"*
- *"What's your #1 superpower?"*
- *"What are the top 3 areas you'd like to grow in?"*
- *"What misconception do your coworkers have about you?"*
- *"How do you push your boundaries and limits?"*
