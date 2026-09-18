export const LOCAL_GOLDEN_ANSWERS: Record<string, string> = {
  life_story:
    "Yeah, so... my journey started at IIT Kanpur where I studied Electrical Engineering, and later I spent time studying International Politics at JNU while preparing for the civil services. That research-heavy phase really taught me how to break down high-stakes, ambiguous problems. When I moved into software engineering, I founded Godizy, a SaaS platform for Indian SMBs that I grew to 10 paying customers, and led the backend team at WorldRef building production AI and RAG pipelines. Right now, what drives me is designing resilient backend microservices with FastAPI and Spring Boot, and building agentic AI architectures with LangGraph.",
  superpower:
    "Hmm... if I had to pick one superpower, it's definitely my ability to take complex, ambiguous technical paradigms and rapidly turn them into reliable production software. You know... whether it was architecting a LangGraph Supervisor-Specialist agentic platform, cutting a critical reporting API latency by 96% at WorldRef, or building a full SaaS product from scratch at Godizy... I dive straight into first principles, build quick prototypes to test failure modes, and ship rock-solid systems.",
  growth_areas:
    "Right, so... there are three specific areas I'm actively focusing on right now. First is executive communication, distilling complex distributed system trade-offs into crisp, intuitive summaries for non-technical stakeholders. Second is business empathy, ensuring every microservice optimization maps directly to customer conversion and business ROI. And third is ruthless prioritization, learning to say no to interesting technical side-quests to focus 100% on the single highest-impact problem.",
  misconceptions:
    "Honestly... one misconception people might have when they first work with me is that... because I tend to stay quiet during early design brainstorms, they might wonder if I'm fully engaged. In reality, I'm just quietly mapping the system out in my head, stress-testing edge cases, thinking through database schema boundaries, and structuring a clean solution before I speak up.",
  pushing_boundaries:
    "You know... I push my boundaries by throwing myself into uncharted territory where there are no ready-made tutorials. Whether it was founding Godizy solo and doing direct sales outreach to local Indian business owners, or designing real-time multi-agent workflows with MCP tool integration and ACL pgvector RAG from scratch... I thrive when I'm tackling ambiguity and learning on the fly.",
  worldref_experience:
    "At WorldRef, I progressed from Software Engineer to Lead Backend Engineer, leading a team of two. I built our entire AI layer end-to-end, including embedding-based RFQ matching evaluated across 3,000+ RFQs, seller scoring across 5,000+ records, and quotation parsing. I also redesigned our data models for 6 core microservices, introduced Redis caching to cut p95 latency by 40%, and optimized an unindexed 4-minute batch query down to under 10 seconds.",
  godizy_experience:
    "Godizy was an incredible learning experience for me. I founded it to help Indian SMBs like clinics, restaurants, and schools establish a digital presence and automate operations. I built the multi-tenant platform using Spring Boot, FastAPI, React, and MySQL, and handled everything from system architecture to pricing tiers and direct customer sales, growing it to 10 paying customers.",
  education_and_jnu:
    "I graduated with a B.Tech in Electrical Engineering from IIT Kanpur, which gave me strong fundamentals in algorithms, computing, and math. Later, I pursued a Master's in International Politics at JNU while preparing for the civil services. That experience was intense and research-heavy—it completely transformed how I analyze complex systemic trade-offs and approach debugging today.",
  handling_uncertainty:
    "Honestly, whenever I encounter something I don't know, I believe in absolute intellectual honesty. I never guess or fake confidence. I clearly state what I don't know, break down the problem into first principles, study the official documentation or source code, and build small test cases until I have a verified answer.",
  tech_stack_deepdive:
    "My core stack is Python with FastAPI and Java with Spring Boot on the backend, React and TypeScript on the frontend, and PostgreSQL with Redis for persistence and caching. On the GenAI side, I work deeply with LangGraph, LangChain, pgvector for RAG pipelines, MCP tool connectors, and containerized deployments using Docker, Kubernetes, and AWS.",
  strengths:
    "Look... my core strengths come down to rapid learning, analytical depth, and high grit. I genuinely enjoy peeling back abstractions to understand how frameworks work under the hood, and when a production incident hits, I stay calm, isolate the telemetry, and solve the root cause systematically.",
  weaknesses:
    "Hmm... candidly, sometimes I get so fascinated by architecting the most elegant, scalable distributed solution that I have to actively remind myself to pause, zoom out, and ask: what is the simplest, most pragmatic solution that solves the user's immediate problem today?",
  motivation:
    "What really drives me is the craft of building high-impact software. There is nothing quite like taking messy, unstructured requirements and engineering a fast, reliable, and elegant system that real users depend on every single day.",
  career_goals:
    "Looking forward, my goal is to grow as an impactful technical leader architecting large-scale distributed AI systems and autonomous agent platforms—bridging deep backend engineering with intuitive product experiences.",
  work_style:
    "My work style is focused, transparent, and high-ownership. I value deep-work blocks for system design and coding, combined with clear asynchronous documentation, paired architecture reviews, and humble, constructive team communication."
};

export function classifyLocalIntent(text: string): string {
  const t = text.toLowerCase();

  // 1. Tech Stack & Skills (Check first so questions like "which tech stack/Java/React" aren't shadowed)
  if (
    t.includes('tech stack') || t.includes('take stack') || t.includes('text stack') ||
    t.includes('skills') || t.includes('technolog') || t.includes('framework') ||
    t.includes('java') || t.includes('react') || t.includes('python') ||
    t.includes('fastapi') || t.includes('spring') || t.includes('langgraph') ||
    t.includes('postgres') || t.includes('redis') || t.includes('pgvector') ||
    t.includes('docker') || t.includes('kubernetes') || t.includes('aws') ||
    t.includes('database') || t.includes('dbms') || t.includes('sql') || t.includes('mysql') || t.includes('caching')
  ) {
    return 'tech_stack_deepdive';
  }

  // 2. Core 5 Suggested Interview Questions
  if (t.includes('life') || t.includes('journey') || t.includes('story') || t.includes('background') || t.includes('about yourself') || t.includes('who are you') || t.includes('resume')) {
    return 'life_story';
  }
  if (t.includes('superpower') || t.includes('super power') || t.includes('greatest strength') || t.includes('best skill')) {
    return 'superpower';
  }
  if (t.includes('growth') || t.includes('grow in') || t.includes('improve') || t.includes('areas to grow') || t.includes('top 3 areas')) {
    return 'growth_areas';
  }
  if (t.includes('misconception') || t.includes('misunderstand') || t.includes('coworker') || t.includes('colleague')) {
    return 'misconceptions';
  }
  if (t.includes('boundar') || t.includes('limit') || t.includes('comfort zone') || t.includes('push')) {
    return 'pushing_boundaries';
  }

  // 3. Work Experience & Specific Companies
  if (t.includes('godizy') || t.includes('founder') || t.includes('smb') || t.includes('saas') || t.includes('10 paying') || t.includes('startup')) {
    return 'godizy_experience';
  }
  if (t.includes('worldref') || t.includes('rfq') || t.includes('latency') || t.includes('4 minute') || t.includes('unindexed') || t.includes('work experience') || t.includes('job experience')) {
    return 'worldref_experience';
  }

  // 4. Education & JNU
  if (t.includes('iit') || t.includes('kanpur') || t.includes('jnu') || t.includes('school') || t.includes('college') || t.includes('university') || t.includes('upsc') || t.includes('degree')) {
    return 'education_and_jnu';
  }

  // 5. Handling Unknowns (Strict check)
  if (/\b(?:when|if|what if)\s+you\s+(?:don't|dont|do not)\s+know\b/.test(t) || t.includes('handle unknowns') || t.includes('when you get stuck')) {
    return 'handling_uncertainty';
  }

  if (t.includes('weakness') || t.includes('flaw') || t.includes('downside') || t.includes('struggle')) {
    return 'weaknesses';
  }
  if (t.includes('motivat') || t.includes('drive') || t.includes('passion') || t.includes('why do you build')) {
    return 'motivation';
  }
  if (t.includes('career') || t.includes('future') || t.includes('where do you see') || t.includes('next 5 years')) {
    return 'career_goals';
  }
  if (t.includes('work style') || t.includes('how do you work') || t.includes('teamwork') || t.includes('collaboration')) {
    return 'work_style';
  }
  if (t.includes('strength') || t.includes('competenc')) {
    return 'strengths';
  }
  return '';
}

export function getLocalFallbackAnswer(question: string): string {
  const intent = classifyLocalIntent(question);
  if (intent && LOCAL_GOLDEN_ANSWERS[intent]) {
    return LOCAL_GOLDEN_ANSWERS[intent];
  }

  const q = question.toLowerCase();

  // Greetings
  if (/\b(hi|hello|hey|greetings|morning|evening|namaste)\b/.test(q)) {
    return "Hey there! I'm Aakash's AI voice assistant. Feel free to ask me about my engineering journey at IIT Kanpur and JNU, leading backend at WorldRef, founding Godizy, or my agentic AI projects.";
  }

  // Location / Contact
  if (['location', 'where do you live', 'where are you based', 'contact', 'email', 'reach out', 'hire', 'phone'].some(w => q.includes(w))) {
    return "I'm based in New Delhi, India. You can reach out to me directly at akskr.iitk@gmail.com, or check out my work on GitHub and LinkedIn.";
  }

  // Unknown or ungrounded questions outside resume
  return "I'm sorry, I am not aware of this and it isn't part of my background or resume, so I can't answer this question. Please feel free to ask me anything about my experience at WorldRef, founding Godizy, IIT Kanpur, or my backend and agentic AI projects!";
}
