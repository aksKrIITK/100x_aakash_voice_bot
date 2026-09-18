from typing import Dict, Any

AAKASH_PROFILE: Dict[str, Any] = {
    "name": "Aakash Kumar",
    "title": "AI & FullStack Engineer | Founder of Godizy | Former Lead Backend Engineer at WorldRef",
    "location": "New Delhi, India",
    "contact": {
        "email": "akskr.iitk@gmail.com",
        "phone": "+91-6206230851",
        "github": "https://github.com/akskr-iitk",
        "linkedin": "https://linkedin.com/in/aakash-kumar",
        "portfolio": "https://aakash-portfolio.vercel.app",
        "product": "https://godizy.com"
    },
    "summary": (
        "AI/Full stack developer with 2+ years of experience shipping production RAG pipelines, "
        "LangGraph multi-agent systems, Python/FastAPI backends, Java/Spring Boot microservices, "
        "and React/TypeScript frontends. Led a 2-engineer backend team at WorldRef. "
        "Founder of Godizy (live B2B SaaS for Indian SMBs with 10 paying customers, built solo end-to-end). "
        "IIT Kanpur Electrical Engineering graduate with 2 years studying International Politics at JNU and UPSC preparation—"
        "a research-heavy background that defines my approach to system design: gather evidence, weigh trade-offs, then commit."
    ),
    "education": [
        {
            "degree": "B.Tech in Electrical Engineering",
            "institution": "IIT Kanpur",
            "period": "2013 – 2017",
            "highlights": "Computation, Data Structures & Algorithms, DBMS, Operating Systems, Computer Networks. Built strong analytical and mathematical foundations."
        },
        {
            "degree": "UPSC Civil Services Preparation (Independent Research)",
            "institution": "Self-directed Study",
            "period": "2017 - 2020",
            "highlights": "Deep research-based learning, analyzing multi-faceted national and structural problems, developing high grit and diverse analytical perspectives."
        },
        {
            "degree": "Master of Arts (MA) in International Politics",
            "institution": "Jawaharlal Nehru University (JNU), New Delhi",
            "period": "2020 - 2022",
            "highlights": "Studied global political structures, policy research, and qualitative systems. Strengthened first-principles reasoning and structural thinking."
        }
    ],
    "experience": [
        {
            "company": "WorldRef Technologies Pvt. Ltd., Noida",
            "role": "Software Engineer to Lead Backend Engineer",
            "period": "Jul 2024 - Jun 2026",
            "achievements": [
                "Built the product AI layer end-to-end: RFQ Matching Engine (embedding-based retrieval evaluated across 3,000+ RFQs), Seller Matching Engine (scoring & ranking 5,000+ seller records), Smart Notifications system, and an RFQ/Quotation Parsing pipeline extracting line items grounded against supplier quotes.",
                "Sole backend architect at early-stage B2B SaaS startup; designed data models, service boundaries, and API contracts for 6 core modules (deal management, chat, notifications, quotation, negotiation, order management) serving multi-tenant clients.",
                "Cut a core reporting API response time from 4 minutes to under 10 seconds (~96% reduction) by introducing request throttling and rewriting an unindexed batch query, unblocking a critical client SLA.",
                "Reduced p95 latency on high-traffic endpoints by 40% using Redis read-through caching and indexed lookups; increased peak-hour throughput by 35% by decomposing monolithic order-processing into async worker services.",
                "Led and mentored 2 junior backend engineers, ran code reviews, paired on architecture decisions, and onboarded them onto service ownership.",
                "Designed secure JWT-authenticated REST APIs with RBAC; built resumable document uploads with AWS S3 pre-signed URLs.",
                "Containerized and deployed services with Docker and Kubernetes behind NGINX on AWS EC2, with CI/CD via GitHub Actions and Jenkins."
            ]
        },
        {
            "company": "Godizy (godizy.com)",
            "role": "Founder & Solo Full-Stack Engineer",
            "period": "Jan 2023 – May 2024 (Full-time); Present (Part-time)",
            "achievements": [
                "Founded and built a multi-tenant SaaS platform (Spring Boot, FastAPI, React, MySQL) helping Indian SMBs (restaurants, clinics, schools) establish a digital presence and automate day-to-day operations.",
                "Architected client/admin/staff portals from scratch and grew the product to 10 paying SMB customers, owning product engineering, pricing tiers, sales scripts, and direct customer outreach solo."
            ]
        }
    ],
    "projects": [
        {
            "name": "Enterprise AI Worker",
            "tech": "FastAPI, LangGraph, Spring Boot, pgvector, SSE, Slack, Jira, GitHub",
            "description": "Multi-tenant, multi-agent 'AI employee' platform. Spring Boot edge gateway (JWT/OIDC, RBAC, tenant isolation) fronting a FastAPI + LangGraph Supervisor-Specialist multi-agent system streaming over SSE. Features MCP tool connectors, ACL-aware pgvector RAG, and Human-in-the-Loop approvals."
        },
        {
            "name": "AI Medical Diagnostic Assistant",
            "tech": "FastAPI, Groq Llama 3.3, LangGraph, Streamlit, Voice/Vision",
            "description": "Multimodal diagnostic workflow integrating patient symptoms, voice recordings, and medical imaging into structured clinical summaries."
        },
        {
            "name": "DealX Connect",
            "tech": "Spring Boot, MySQL, Redis, AWS, JWT, Quotation Engine",
            "description": "B2B SaaS deal-negotiation platform with real-time quotation generation and high-throughput Redis caching."
        }
    ],
    "skills": {
        "languages": ["Python", "Java", "TypeScript", "JavaScript", "SQL"],
        "backend": ["FastAPI", "Spring Boot", "Hibernate/JPA", "Microservices", "REST APIs", "System Design"],
        "genai_agents": ["LangGraph", "LangChain", "RAG", "MCP", "Multi-Agent Architectures", "pgvector", "FAISS", "Pinecone", "Edge TTS"],
        "frontend": ["React", "TypeScript", "Tailwind CSS", "Vite", "HTML5/CSS3"],
        "databases_caching": ["PostgreSQL", "MySQL", "Redis", "MongoDB"],
        "devops_cloud": ["AWS (EC2, S3, RDS, Lambda)", "Docker", "Kubernetes", "NGINX", "Jenkins", "GitHub Actions"]
    },
    "mindset_and_values": {
        "engineering_philosophy": "Gather evidence, weigh trade-offs, then commit. I avoid resume-driven development and focus on simple, observable, robust architectures that actually solve user problems.",
        "superpower": "Rapidly learning complex technical paradigms from first principles and shipping them as production-grade software (e.g., building multi-agent LangGraph workflows, cutting API latencies by 96%, or founding a full-stack SaaS).",
        "growth_areas": [
            "Executive Communication: Distilling complex distributed system trade-offs into crisp, intuitive summaries for business stakeholders.",
            "Business Empathy: Ensuring every backend optimization maps directly to customer conversion, retention, and business ROI.",
            "Ruthless Prioritization: Saying no to exciting side explorations to focus 100% on the single highest-impact problem."
        ],
        "work_style": "High-ownership, transparent, and collaborative. Deep focus blocks for architecture and coding, paired with humble code reviews and thorough documentation.",
        "handling_uncertainty": "When I don't know something, I never guess or fake confidence. I acknowledge the gap, inspect the documentation and source code, build small throwaway prototypes to understand failure modes, and verify with data."
    }
}
