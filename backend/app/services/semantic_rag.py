import re
import math
from typing import List, Dict, Any, Tuple

# Comprehensive Knowledge Base covering Aakash's Resume, Background, Projects, Leadership & Philosophy
AAKASH_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "worldref_overview",
        "topic": "WorldRef Work Experience & AI Layer Overview",
        "keywords": [
            "worldref", "work", "experience", "job", "career", "role", "company", "lead backend",
            "software engineer", "noida", "worked", "current job", "last company", "b2b saas"
        ],
        "content": (
            "At WorldRef Technologies (Noida, Jul 2024 - Jun 2026), I progressed from Software Engineer to Lead Backend Engineer, leading a 2-engineer backend team. "
            "I built the product's entire AI layer end-to-end including an embedding-based RFQ Matching Engine evaluated across 3,000+ RFQs, a Seller Matching Engine scoring 5,000+ records, "
            "a Smart Notifications system, and an RFQ/Quotation Parsing pipeline that extracts line items from buyer RFQs and grounds them against supplier quotations."
        )
    },
    {
        "id": "worldref_rfq_engine",
        "topic": "WorldRef AI Layer, RFQ Matching & Quotation Parsing",
        "keywords": [
            "rfq", "matching", "seller matching", "quotation", "parsing", "buyer", "supplier", "line items",
            "embeddings", "ai layer", "scoring", "3000", "5000", "extraction", "grounding"
        ],
        "content": (
            "At WorldRef, I engineered the entire AI pipeline: an embedding-based RFQ Matching Engine benchmarked on 3,000+ RFQs to match buyer requests to verified suppliers, "
            "a Seller Matching Engine that dynamically scored and ranked 5,000+ seller records, and an automated Quotation Parsing pipeline that accurately extracts line items "
            "from buyer RFQ documents and cross-grounds them against supplier quotes to streamline procurement."
        )
    },
    {
        "id": "worldref_latency_query",
        "topic": "WorldRef 4-Minute Latency Reduction & Query Optimization",
        "keywords": [
            "latency", "4 minute", "query", "optimization", "speed", "performance", "sla", "unindexed",
            "bottleneck", "slow", "reporting api", "96 percent", "throttling", "challenge", "hardest bug",
            "problem solved", "production fix"
        ],
        "content": (
            "At WorldRef, the most impactful performance challenge I solved was cutting a critical reporting API's response time from 4 minutes down to under 10 seconds (~96% reduction). "
            "I achieved this by analyzing database query plans, reworking an unindexed batch query, and introducing request throttling, which unblocked a major enterprise SLA that had been repeatedly missed."
        )
    },
    {
        "id": "worldref_caching_throughput",
        "topic": "WorldRef Redis Caching & Async Microservice Throughput",
        "keywords": [
            "redis", "caching", "throughput", "p95", "latency", "async worker", "peak hour", "scale",
            "scaling", "40 percent", "35 percent", "read through", "microservice architecture"
        ],
        "content": (
            "To handle high peak-hour loads at WorldRef, I introduced a Redis read-through caching layer and indexed database lookups, cutting p95 endpoint latency by 40%. "
            "I also increased peak-hour throughput by 35% by decomposing monolithic order processing into asynchronous background worker services."
        )
    },
    {
        "id": "worldref_microservices_architecture",
        "topic": "WorldRef Microservices Architecture & System Design",
        "keywords": [
            "microservices", "architecture", "data model", "service boundaries", "api contracts", "modules",
            "deal management", "chat", "notifications", "quotation", "negotiation", "order management",
            "jwt", "rbac", "s3", "presigned urls", "docker", "kubernetes", "jenkins", "aws"
        ],
        "content": (
            "As the sole backend architect at WorldRef during our early stage, I designed the data models, service boundaries, and API contracts for 6 core microservices: "
            "deal management, chat, notifications, quotation, negotiation, and order management. "
            "I implemented secure JWT authentication with RBAC, built resumable S3 pre-signed upload pipelines, and deployed containerized services via Docker and Kubernetes on AWS."
        )
    },
    {
        "id": "worldref_mentorship",
        "topic": "WorldRef Engineering Leadership & Mentorship",
        "keywords": [
            "team", "mentor", "mentoring", "leadership", "lead", "junior", "engineers", "code review",
            "pairing", "onboarding", "culture", "management", "delegation", "guidance"
        ],
        "content": (
            "As Lead Backend Engineer at WorldRef, I led and mentored 2 junior backend engineers. "
            "I established weekly architecture pairing sessions, instituted rigorous code review standards, and guided them in taking complete ownership of microservices, significantly cutting their onboarding ramp-up time."
        )
    },
    {
        "id": "godizy_founder",
        "topic": "Godizy Startup Founder Experience & Growth",
        "keywords": [
            "godizy", "founder", "startup", "smb", "10 paying", "saas", "customers", "solo", "sales",
            "business", "outreach", "pricing", "entrepreneur", "founded", "revenue", "clients", "cold outreach"
        ],
        "content": (
            "I founded Godizy (godizy.com), a multi-tenant B2B SaaS platform helping Indian SMBs—such as restaurants, clinics, and schools—establish a digital presence and automate day-to-day operations. "
            "I owned everything end-to-end: architecting the product from scratch, writing sales pitches, conducting direct customer outreach, defining pricing tiers, and growing it to 10 paying customers."
        )
    },
    {
        "id": "godizy_tech_architecture",
        "topic": "Godizy Technical Architecture & Multi-Tenancy",
        "keywords": [
            "godizy tech", "godizy stack", "multi tenant", "tenant isolation", "spring boot", "fastapi",
            "react", "mysql", "saas architecture", "smb platform"
        ],
        "content": (
            "For Godizy, I built a scalable multi-tenant architecture using Java Spring Boot and Python FastAPI on the backend, React on the frontend, and MySQL for relational tenant data isolation. "
            "The platform automated appointment scheduling, customer inquiries, and online storefront management for non-technical business owners."
        )
    },
    {
        "id": "project_enterprise_ai_worker",
        "topic": "Enterprise AI Worker Platform (LangGraph Multi-Agent SaaS)",
        "keywords": [
            "enterprise ai", "ai worker", "ai employee", "langgraph", "multi agent", "supervisor", "specialist",
            "sse", "streaming", "pgvector", "rag", "mcp", "model context protocol", "slack", "jira", "github", "hitl", "human in the loop"
        ],
        "content": (
            "I built the Enterprise AI Worker platform—a multi-tenant 'AI employee' SaaS integrating Slack, Gmail, Jira, GitHub, and internal docs. "
            "It features a Spring Boot edge gateway (JWT/OIDC, RBAC, tenant isolation) fronting a FastAPI + LangGraph Supervisor-Specialist multi-agent system streaming over SSE. "
            "It includes MCP tool connectors, ACL-aware pgvector RAG with dual-layer filtering, and Human-in-the-Loop approvals for write actions, validated by a 27-test suite."
        )
    },
    {
        "id": "project_medical_and_dealx",
        "topic": "AI Medical Diagnostic Assistant & DealX Connect Projects",
        "keywords": [
            "medical", "diagnostic", "dealx", "deal negotiation", "groq", "streamlit", "vision", "voice",
            "multimodal", "medical imagery", "xray", "ct scan"
        ],
        "content": (
            "I built the AI Medical Diagnostic Assistant—a multimodal LangGraph workflow integrating text, voice, and medical imagery analysis using FastAPI, Groq Llama 3.3, and Streamlit. "
            "I also built DealX Connect—a B2B deal negotiation platform engineered with Spring Boot, MySQL, Redis, and AWS with real-time quotation generation and high-throughput caching."
        )
    },
    {
        "id": "education_iit_kanpur",
        "topic": "IIT Kanpur Education (B.Tech Electrical Engineering)",
        "keywords": [
            "iit", "kanpur", "electrical", "engineering", "btech", "degree", "college", "undergraduate",
            "algorithms", "dsa", "os", "dbms", "networks", "school", "academics", "graduated", "iitk", "math"
        ],
        "content": (
            "I graduated from IIT Kanpur with a B.Tech in Electrical Engineering (2013-2017). "
            "My coursework covered computation, data structures & algorithms, operating systems, DBMS, and computer networks. "
            "IIT Kanpur gave me strong mathematical foundations, analytical rigor, and the ability to break down complex computing systems from first principles."
        )
    },
    {
        "id": "education_jnu_upsc",
        "topic": "UPSC Preparation & JNU MA in International Politics",
        "keywords": [
            "jnu", "international politics", "upsc", "civil service", "masters", "policy", "political science",
            "research", "world structure", "delhi", "ias", "why upsc", "switch to software", "career pivot"
        ],
        "content": (
            "Between 2017 and 2020, I engaged in deep independent research while preparing for India's civil services (UPSC), and subsequently completed my Master's in International Politics at JNU (2020-2022). "
            "This research-heavy phase trained me to analyze multi-layered geopolitical and structural problems. "
            "Today, that exact training shows up in how I approach software architecture and debugging: gather evidence, weigh trade-offs systematically, and then commit."
        )
    },
    {
        "id": "tech_stack_core",
        "topic": "Core Backend, Frontend, Cloud & AI Tech Stack",
        "keywords": [
            "tech stack", "technology", "technologies", "languages", "frameworks", "skills",
            "fastapi", "spring boot", "python", "java", "react", "typescript",
            "postgres", "postgresql", "redis", "mysql", "docker", "kubernetes", "aws",
            "langgraph", "langchain", "pgvector", "rag", "mcp", "take stack", "text stack",
            "what others", "worked with", "worked on", "tools you use"
        ],
        "content": (
            "My core tech stack spans Python with FastAPI and Java with Spring Boot for scalable backends, React and TypeScript on the frontend, and PostgreSQL, MySQL, and Redis for storage and caching. "
            "For GenAI and agentic systems, I specialize in LangGraph, LangChain, RAG pipelines with pgvector, MCP tool connectors, and container orchestration with Docker and Kubernetes on AWS."
        )
    },
    {
        "id": "databases_caching",
        "topic": "Databases, Caching & Data Layer Architecture",
        "keywords": [
            "database", "databases", "db", "dbms", "sql", "nosql", "postgres", "postgresql", "mysql",
            "redis", "pgvector", "caching", "cache", "indexing", "queries", "read through", "data model"
        ],
        "content": (
            "For persistence, I work primarily with PostgreSQL and MySQL for relational, ACID-compliant multi-tenant workloads, and PostgreSQL with pgvector for vector search in RAG pipelines. "
            "For caching and high-throughput low-latency access, I use Redis with read-through caching and optimized indexes, reducing p95 database load by over 40%."
        )
    },
    {
        "id": "agentic_ai_rag",
        "topic": "Agentic AI, Multi-Agent Systems & RAG Pipelines",
        "keywords": [
            "agent", "agentic", "langgraph", "langchain", "rag", "retrieval", "pgvector", "mcp",
            "multi agent", "supervisor", "tools", "vector search", "llm pipeline", "autonomous"
        ],
        "content": (
            "In agentic AI, I specialize in designing deterministic multi-agent state graphs using LangGraph with Supervisor-Specialist topologies. "
            "I build production RAG systems with ACL-filtered pgvector hybrid search, Model Context Protocol (MCP) integrations, and streaming responses over Server-Sent Events (SSE)."
        )
    },
    {
        "id": "system_design_philosophy",
        "topic": "System Design Philosophy & Architecture Approach",
        "keywords": [
            "system design", "architecture approach", "philosophy", "design principles", "scalability",
            "resilience", "first principles", "how do you design", "trade offs", "modular"
        ],
        "content": (
            "My system design philosophy is rooted in first principles: define strict domain boundaries, establish clear API contracts early, decouple compute from state, and design for observability. "
            "I avoid premature optimization, choosing simple, highly modular architectures that can scale horizontally with asynchronous workers and caching."
        )
    },
    {
        "id": "debugging_problem_solving",
        "topic": "Debugging, Outages & Production Problem Solving",
        "keywords": [
            "debugging", "outage", "production incident", "problem solving", "root cause", "troubleshoot",
            "server crash", "sunday crash", "on call", "how do you debug", "solve problems"
        ],
        "content": (
            "When production issues or unexpected bugs occur, my approach is methodical and telemetry-driven. "
            "I first isolate the failure domain using logs and metrics, replicate the edge case with minimal test inputs, identify the underlying root cause rather than patching symptoms, and verify the fix with automated regression tests."
        )
    },
    {
        "id": "superpower",
        "topic": "#1 Superpower",
        "keywords": [
            "superpower", "super power", "greatest strength", "best skill", "unique capability",
            "what makes you special", "core strength", "standout"
        ],
        "content": (
            "My #1 superpower is rapidly grasping complex, ambiguous technical paradigms and shipping them as production-grade software. "
            "Whether it was architecting real-time multi-agent systems with LangGraph, reducing query latency by 96% at WorldRef, or building a SaaS business from scratch at Godizy, I dive straight into first principles and deliver reliable results."
        )
    },
    {
        "id": "growth_areas",
        "topic": "Top 3 Growth Areas",
        "keywords": [
            "growth", "grow in", "growth areas", "improve", "weakness", "areas to grow", "prioritization",
            "communication", "business empathy", "top 3 areas", "learning goals"
        ],
        "content": (
            "I am actively focusing on three growth areas: "
            "First, executive communication, distilling complex distributed system trade-offs into crisp, intuitive summaries for business stakeholders. "
            "Second, business empathy, ensuring every backend optimization directly drives customer conversion and ROI. "
            "And third, ruthless prioritization, saying no to interesting side explorations to stay 100% focused on the highest-impact problem."
        )
    },
    {
        "id": "coworker_misconceptions",
        "topic": "Coworker Misconceptions",
        "keywords": [
            "misconception", "coworker", "colleague", "quiet", "brainstorm", "first impression",
            "think about you", "misunderstand", "perception"
        ],
        "content": (
            "One misconception people might have when they first work with me is that because I tend to stay quiet during early design brainstorms, they might wonder if I'm engaged. "
            "In reality, I'm just quietly mapping the system out in my head, stress-testing edge cases, thinking through database schema boundaries, and structuring a clean solution before I speak up."
        )
    },
    {
        "id": "pushing_boundaries",
        "topic": "Pushing Boundaries & Limits",
        "keywords": [
            "push", "boundaries", "limits", "comfort zone", "challenges", "ambiguity",
            "learn on the fly", "difficult", "hard situations"
        ],
        "content": (
            "I push my boundaries by throwing myself into uncharted territory where there are no ready-made tutorials. "
            "Whether it was founding Godizy solo and doing cold sales outreach to local Indian business owners, or designing real-time multi-agent workflows with MCP tool integration and ACL pgvector RAG from scratch, I thrive when tackling ambiguity."
        )
    },
    {
        "id": "handling_unknowns",
        "topic": "Handling Unknowns & Intellectual Honesty",
        "keywords": [
            "when you don't know", "how do you handle unknowns", "what if you don't know the answer",
            "when you get stuck", "facing unknown", "intellectual honesty", "unsure"
        ],
        "content": (
            "When I don't know an answer, I practice absolute intellectual honesty—I will never guess or fake confidence. "
            "Instead, I clearly acknowledge what I don't know yet, break down the core fundamentals, dive straight into official documentation or source code, and systematically test it until I have a verified solution."
        )
    },
    {
        "id": "work_style_culture",
        "topic": "Work Style, Teamwork & Code Quality",
        "keywords": [
            "work style", "teamwork", "collaboration", "how do you work", "culture", "deep work",
            "code review", "pairing", "code quality", "testing philosophy", "unit tests"
        ],
        "content": (
            "My work style is focused, transparent, and high-ownership. "
            "I value deep-work blocks for system design and coding, combined with clear asynchronous documentation, paired architecture reviews, automated test coverage, and humble, constructive team communication."
        )
    },
    {
        "id": "career_vision",
        "topic": "Career Goals & Next 5 Years",
        "keywords": [
            "career", "future", "goals", "where do you see yourself", "next 5 years", "ambition",
            "vision", "staff engineer", "long term"
        ],
        "content": (
            "Looking forward, my goal is to grow as an impactful technical leader architecting large-scale distributed AI systems and autonomous agent platforms—bridging deep backend engineering with intuitive product experiences."
        )
    },
    {
        "id": "location_contact",
        "topic": "Location, Availability & Contact Details",
        "keywords": [
            "location", "where do you live", "where are you based", "contact", "email", "phone",
            "reach out", "hire", "github", "linkedin", "delhi", "notice period"
        ],
        "content": (
            "I'm based in New Delhi, India. You can reach out to me directly at akskr.iitk@gmail.com or +91-6206230851, and explore my work on GitHub and LinkedIn."
        )
    }
]


# Conversational greeting keywords
GREETING_PATTERNS = [r"\b(?:hi|hello|hey|greetings|good\s+morning|good\s+evening|namaste)\b"]

HUMBLE_UNKNOWN_REJECTION = (
    "I'm sorry, I am not aware of this and it isn't part of my background or resume, so I can't answer this question. "
    "Please feel free to ask me anything about my experience at WorldRef, founding Godizy, IIT Kanpur, or my backend and agentic AI projects!"
)


def tokenize(text: str) -> List[str]:
    """Cleans and extracts meaningful lowercase word tokens."""
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    # Stop words and generic conversational noise
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'is', 'are', 'was', 'were', 'in', 'on', 'at',
        'to', 'for', 'of', 'with', 'about', 'can', 'you', 'tell', 'me', 'what', 'how',
        'why', 'your', 'my', 'do', 'did', 'does', 'please', 'just', 'some', 'any',
        'don', 'dont', 't', 'no', 'not', 'like', 'ask', 'asking', 'which', 'others',
        'd', 'm', 're', 've', 'll', 'have', 'had', 'been', 'would', 'could', 'should',
        'listen', 'talking', 'appearing', 'applying', 'interview', 'tell', 'company', 'zinc', 'zing'
    }
    return [t for t in cleaned.split() if t and t not in stop_words and len(t) > 1]


def compute_chunk_score(query_tokens: List[str], raw_query_lower: str, chunk: Dict[str, Any]) -> float:
    """Calculates semantic relevance score for a knowledge chunk against query tokens and query text."""
    if not query_tokens:
        return 0.0

    score = 0.0
    chunk_keywords = [k.lower() for k in chunk.get("keywords", [])]
    chunk_content = chunk.get("content", "").lower()
    chunk_topic = chunk.get("topic", "").lower()

    # Core high-priority technical terms and unique domain entities
    domain_identifiers = {
        "java", "react", "python", "fastapi", "spring", "boot", "typescript",
        "postgres", "postgresql", "redis", "mysql", "docker", "kubernetes", "aws",
        "langgraph", "langchain", "pgvector", "stack", "skills", "backend", "frontend",
        "database", "databases", "rfq", "latency", "godizy", "worldref", "iit", "kanpur",
        "jnu", "upsc", "superpower", "growth", "misconception", "boundaries", "dealx"
    }

    # Direct multi-word phrase matching (e.g. "tech stack", "system design", "4 minute", "worldref")
    for kw in chunk_keywords:
        if len(kw.split()) > 1 and kw in raw_query_lower:
            score += 10.0
        elif kw in domain_identifiers and re.search(r'\b' + re.escape(kw) + r'\b', raw_query_lower):
            score += 8.0

    matched_tokens = 0
    for token in query_tokens:
        # 1. Exact match in designated keywords
        for kw in chunk_keywords:
            if token == kw:
                matched_tokens += 1
                weight = 6.0 if token in domain_identifiers else 3.0
                score += weight
            elif len(token) >= 4 and token in kw:
                matched_tokens += 1
                score += 2.0

        # 2. Match in topic title
        if token in chunk_topic:
            score += 3.0

        # 3. Frequency in chunk content
        count = chunk_content.count(token)
        if count > 0:
            score += min(3.0, count * 0.8)

    # If only 1 weak generic word matched, keep score low
    if matched_tokens <= 1 and score < 6.0:
        return 0.0

    return score


class SemanticRAGService:
    """Fast, accurate semantic retrieval engine indexing Aakash's background."""

    def __init__(self, knowledge_base: List[Dict[str, Any]] = None):
        self.knowledge_base = knowledge_base or AAKASH_KNOWLEDGE_BASE

    def retrieve(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """Retrieves top-k most relevant knowledge chunks with scores."""
        query_tokens = tokenize(query)
        raw_query_lower = query.lower().strip()
        if not query_tokens:
            return [(self.knowledge_base[0], 0.0)]

        scored: List[Tuple[Dict[str, Any], float]] = []
        for chunk in self.knowledge_base:
            score = compute_chunk_score(query_tokens, raw_query_lower, chunk)
            scored.append((chunk, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def get_grounding_context(self, query: str, top_k: int = 2) -> str:
        """Constructs a consolidated grounding context string for LLM synthesis."""
        top_results = self.retrieve(query, top_k=top_k)
        contexts = []
        for chunk, score in top_results:
            if score >= 4.0:
                contexts.append(f"[{chunk['topic']}]: {chunk['content']}")

        if not contexts:
            return ""

        return "\n\n".join(contexts)

    def synthesize_fallback_response(self, query: str) -> str:
        """Synthesizes an authentic first-person response grounded in retrieved resume facts or rejects unknown questions humbly."""
        raw_lower = query.lower().strip()

        # 1. Greetings
        if any(re.search(pat, raw_lower) for pat in GREETING_PATTERNS) and len(raw_lower.split()) <= 4:
            return (
                "Hey there! I'm Aakash's AI voice clone. Feel free to ask me anything about my engineering background, "
                "work at WorldRef, founding Godizy, or my projects and tech stack!"
            )

        # 2. Retrieve top grounded chunk
        top_results = self.retrieve(query, top_k=1)
        if top_results and top_results[0][1] >= 4.0:
            return top_results[0][0]["content"]

        # 3. Humble rejection for any unknown topic not in resume/background
        return HUMBLE_UNKNOWN_REJECTION


semantic_rag_service = SemanticRAGService()
