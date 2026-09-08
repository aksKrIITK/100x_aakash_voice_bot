import re
from typing import Optional

# Keyword map for deterministic intent classification
INTENT_PATTERNS = {
    "life_story": [
        r"life story", r"journey", r"tell me about yourself", r"who are you", r"your background",
        r"education", r"iit kanpur", r"jnu", r"where did you study", r"introduce yourself",
        r"story in a few sentences", r"know about your life", r"tell us about your life"
    ],
    "superpower": [
        r"superpower", r"#1 superpower", r"number 1 superpower", r"best at", r"biggest strength",
        r"greatest strength", r"top skill", r"what are you best at", r"stand out", r"what is your superpower",
        r"coworkers say your superpower"
    ],
    "growth_areas": [
        r"growth area", r"improve", r"want to grow", r"areas to grow", r"working on",
        r"top 3 areas", r"development goals", r"top 3 areas you'd like to grow", r"areas you'd like to grow"
    ],
    "misconceptions": [
        r"misconception", r"coworker", r"colleague", r"misunderstand", r"what do people get wrong",
        r"wrong impression", r"misconception do your coworkers have", r"coworkers have about you"
    ],
    "pushing_boundaries": [
        r"push.*limit", r"push.*boundar", r"challenge yourself", r"step out of.*comfort",
        r"comfort zone", r"overcome limit", r"push your boundaries", r"boundaries and limits"
    ],
    "strengths": [
        r"strength", r"strongest skill", r"good at", r"capabilities"
    ],
    "weaknesses": [
        r"weakness", r"flaw", r"stumble", r"downside", r"limitation"
    ],
    "motivation": [
        r"motivat", r"inspir", r"what drives you", r"why do you build", r"passion"
    ],
    "career": [
        r"career", r"future goal", r"where do you see yourself", r"ambition", r"staff engineer"
    ],
    "learning": [
        r"how do you learn", r"learning style", r"new tech", r"pick up tech"
    ],
    "failure": [
        r"failure", r"mistake", r"handled a bug", r"production incident", r"failed project"
    ],
    "risk": [
        r"risk", r"taking risks", r"risk tolerance"
    ],
    "decision_making": [
        r"decision", r"trade-off", r"make decisions", r"choose technology"
    ],
    "work_style": [
        r"work style", r"how do you work", r"teamwork", r"collaboration", r"deep work"
    ],
    "future": [
        r"future", r"next 5 years", r"upcoming goals", r"what is next"
    ]
}


def classify_question_intent(question: str) -> Optional[str]:
    """Deterministically classifies user question into a golden answer category."""
    cleaned = question.lower().strip()
    
    for category, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, cleaned):
                return category
                
    return None
