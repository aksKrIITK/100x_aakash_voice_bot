import re
from typing import Optional, Dict, List

INTENT_PATTERNS: Dict[str, List[str]] = {
    "life_story": [
        r"life story", r"tell me about yourself", r"who are you", r"background",
        r"introduce yourself", r"your journey", r"overview of yourself", r"walk me through your resume"
    ],
    "superpower": [
        r"superpower", r"super power", r"greatest strength", r"best skill",
        r"what makes you unique", r"what are you best at", r"special power"
    ],
    "growth_areas": [
        r"grow in", r"areas to grow", r"growth area", r"improve on",
        r"top 3 areas", r"what do you want to learn", r"areas of improvement"
    ],
    "misconceptions": [
        r"misconception", r"misunderstand", r"coworker", r"colleague think",
        r"first impression", r"wrong impression", r"people get wrong about you"
    ],
    "pushing_boundaries": [
        r"push.*boundar", r"push.*limit", r"comfort zone", r"challenging project",
        r"difficult situation", r"take on challenges", r"step out of your comfort"
    ],
    "worldref_experience": [
        r"worldref", r"lead backend", r"rfq", r"seller matching", r"quotation parsing",
        r"latency reduction", r"4 minute", r"unindexed query", r"mentoring", r"backend team"
    ],
    "godizy_experience": [
        r"godizy", r"founder", r"startup", r"saas", r"10 paying", r"smb", r"solo founder"
    ],
    "education_and_jnu": [
        r"iit", r"kanpur", r"electrical engineering", r"jnu", r"international politics",
        r"school", r"college", r"university", r"degree", r"upsc", r"civil services"
    ],
    "handling_uncertainty": [
        r"\b(?:when|if|what if)\s+you\s+(?:don't|dont|do not)\s+know\b",
        r"\bhow\s+do\s+you\s+handle\s+(?:unknowns?|uncertainty|what you don't know)\b",
        r"\bwhen\s+you\s+(?:get\s+stuck|face\s+something\s+unknown)\b",
        r"\bwhat\s+do\s+you\s+do\s+when\s+you\s+don't\s+know\b"
    ],
    "tech_stack_deepdive": [
        r"\b(?:tech|take|text)\s*stack\b", r"\bskills?\b", r"\btechnolog(?:y|ies)\b",
        r"\bframeworks?\b", r"\blanguages?\b", r"\bjava\b", r"\breact\b", r"\bpython\b",
        r"\bfastapi\b", r"\bspring\s*boot\b", r"\bbackend\s*stack\b", r"\bfrontend\s*stack\b",
        r"\blanggraph\b", r"\blangchain\b", r"\bpostgres\b", r"\bredis\b", r"\bpgvector\b",
        r"\brag\b", r"\bdocker\b", r"\bkubernetes\b", r"\btools?\s+you\s+use\b",
        r"\bdatabases?\b", r"\bdbms\b", r"\bsql\b", r"\bnosql\b", r"\bmysql\b", r"\bcaching\b"
    ],
    "strengths": [
        r"strength", r"what are you good at", r"core competencies", r"technical strength"
    ],
    "weaknesses": [
        r"weakness", r"flaw", r"downside", r"limitation", r"where do you struggle"
    ],
    "motivation": [
        r"motivat", r"inspir", r"what drives you", r"why do you build", r"passion", r"get out of bed"
    ],
    "career_goals": [
        r"career goal", r"future", r"where do you see yourself", r"next 5 years", r"ambition"
    ],
    "work_style": [
        r"work style", r"how do you work", r"teamwork", r"collaboration", r"deep work", r"code review"
    ]
}


def classify_question_intent(question: str) -> Optional[str]:
    """Deterministically classifies user question into a golden answer category."""
    cleaned = question.lower().strip()
    for intent, patterns in INTENT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, cleaned):
                return intent
    return None
