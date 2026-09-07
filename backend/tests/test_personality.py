import pytest
from app.personality.question_classifier import classify_question_intent
from app.personality.golden_answers import GOLDEN_ANSWERS


def test_question_classifier_matches():
    assert classify_question_intent("What is your life story?") == "life_story"
    assert classify_question_intent("Tell me about your journey") == "life_story"
    assert classify_question_intent("What is your #1 superpower?") == "superpower"
    assert classify_question_intent("What are you best at?") == "superpower"
    assert classify_question_intent("What top 3 areas do you want to grow in?") == "growth_areas"
    assert classify_question_intent("What misconception do coworkers have about you?") == "misconceptions"
    assert classify_question_intent("How do you push your boundaries?") == "pushing_boundaries"


def test_golden_answers_presence():
    required_keys = [
        "life_story", "superpower", "growth_areas",
        "misconceptions", "pushing_boundaries"
    ]
    for key in required_keys:
        assert key in GOLDEN_ANSWERS
        assert len(GOLDEN_ANSWERS[key]) > 20
