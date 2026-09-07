# Software Project Development Phases - Aakash AI Voice Bot

This document outlines the systematic, production-grade development phases for **Aakash AI**, a complete AI Voice Bot web application that represents Aakash through a conversational AI voice and text interface.

---

## Overview & Architecture Goals
- **Product Name**: Aakash AI
- **Tagline**: "Talk to an AI that answers as Aakash would."
- **Core Requirement**: Complete, production-ready, deployable application. Evaluators can run and test all capabilities (voice recording, speech-to-text, personality LLM, conversation memory, browser text-to-speech, text fallback) out of the box without providing an OpenAI API key.

```
USER
  │
  ▼
React + Vite SPA (Vercel)
  │ (HTTPS REST API / Web Speech API)
  ▼
FastAPI Backend (Railway/Render)
  ├── Voice Endpoint (/api/v1/voice/chat) -> STT Service (Whisper/Mock)
  ├── Text Endpoint (/api/v1/chat)
  ├── Personality Engine (Profile + System Prompt + Golden Answers + Question Classifier)
  ├── Conversation Service & Context Memory Manager
  └── Database Repository (PostgreSQL / In-Memory Fallback)
```

---

## Development Phases

### Phase 1: Architecture, Workspace Setup & Directory Structure
- [ ] Initialize repository root structure: `backend/`, `frontend/`, `docker-compose.yml`, `README.md`, `PROJECT_PHASES.md`.
- [ ] Setup Python environment for backend with FastAPI, Pydantic, SQLAlchemy, Uvicorn, Pytest, OpenAI, and HTTPX.
- [ ] Setup React + Vite + TypeScript single-page application with Tailwind CSS in `frontend/`.
- [ ] Configure environment variables (`.env.example`) for frontend and backend ensuring no secrets or API keys are exposed to the client.

### Phase 2: Core Backend Engine & Personality Infrastructure
- [ ] Create Pydantic config & FastAPI application structure with routers, middleware, logging, and error handlers.
- [ ] Create `personality/profile.py` with structured profile data for Aakash Kumar (IIT Kanpur, JNU, FastAPI, React, Spring Boot, Postgres, RAG, LangChain, agentic AI, strengths, growth areas, values).
- [ ] Create `personality/golden_answers.py` with curated grounding responses for key questions (life story, #1 superpower, top 3 growth areas, misconceptions, pushing limits, etc.).
- [ ] Create `personality/system_prompt.py` enforcing strict first-person persona rules (no AI disclaimers, no corporate jargon, humble & direct tone).
- [ ] Implement `personality/question_classifier.py` for low-latency intent classification.
- [ ] Implement `ConversationRepository` supporting PostgreSQL via SQLAlchemy with automatic fallback to thread-safe In-Memory storage.

### Phase 3: AI Provider Abstractions & Voice Pipeline
- [ ] Build `LLMProvider` abstraction (`base.py`, `openai_provider.py`, and intelligent `MockLLMProvider` fallback for zero-API key execution).
- [ ] Build `SpeechToTextProvider` abstraction (`base.py`, `openai_provider.py`, and `MockSpeechToTextProvider` fallback).
- [ ] Implement `ConversationService` to manage turn-taking, prompt construction, memory history windowing, answer validation, and response persistence.
- [ ] Implement `VoiceService` to validate incoming audio, run STT transcription, and pass transcript to `ConversationService`.
- [ ] Expose REST API endpoints:
  - `GET /api/v1/health`
  - `POST /api/v1/conversations`
  - `POST /api/v1/chat`
  - `POST /api/v1/voice/chat`

### Phase 4: Frontend UI & Audio Integration
- [ ] Create reusable TypeScript interfaces and state management.
- [ ] Implement `useAudioRecorder` custom hook utilizing browser `MediaRecorder` API with permission handling and MIME type detection.
- [ ] Implement `useSpeechSynthesis` custom hook for browser `SpeechSynthesis` API supporting playback, pause, resume, replay, and stop.
- [ ] Implement `useVoiceBot` hook coordinating voice states (`IDLE`, `LISTENING`, `PROCESSING`, `SPEAKING`, `ERROR`).
- [ ] Develop components:
  - `Header`: Clean brand header with server connection indicator.
  - `Hero`: Inviting hero section ("Hi, I'm Aakash's AI voice assistant 👋").
  - `MicrophoneButton`: Interactive animated recording control.
  - `AudioVisualizer`: Live visual feedback during listening state.
  - `Conversation` & `ConversationMessage`: Responsive chat message history with playback controls.
  - `SuggestedQuestions`: One-click prompt chips.
  - `TextInput`: Accessible text entry fallback.
  - `ErrorMessage`: User-friendly error banner without raw HTTP traces.
  - `Footer`: Links and system overview.

### Phase 5: Error Handling, Fallbacks & Quality Assurance
- [ ] Implement graceful fallbacks for microphone permission failure, speech synthesis absence, database disconnects, and provider outages.
- [ ] Add unit and integration test suite in backend (`tests/test_health.py`, `test_chat.py`, `test_voice.py`, `test_personality.py`).
- [ ] Run full end-to-end verification (voice recording, STT, LLM response, TTS replay, follow-up memory).
- [ ] Validate responsive design across desktop, tablet, and mobile browsers.

### Phase 6: Containerization, Deployment & Final Documentation
- [ ] Create `backend/Dockerfile` and root `docker-compose.yml`.
- [ ] Create `frontend/vercel.json` for frontend deployment on Vercel.
- [ ] Ensure backend readiness for Railway / Render deployment.
- [ ] Write comprehensive `README.md` containing architecture, local setup instructions, API spec, Docker commands, and design philosophy.
