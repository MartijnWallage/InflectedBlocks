"""User vocabulary management and flashcard logic with Leitner box system."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from data import WORDS

DATA_FILE = Path(__file__).parent / "user_data.json"

# Leitner box intervals (days)
BOX_INTERVALS = {1: 1, 2: 2, 3: 5, 4: 14, 5: 30}


def load_user_data() -> dict:
    """Load user state from JSON file, or create defaults."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "vocabulary": [],
        "flashcard_progress": {},
        "sentences_completed": 0,
    }


def save_user_data(data: dict) -> None:
    """Persist user state to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_to_vocabulary(data: dict, lemma: str) -> bool:
    """Add a lemma to the user's vocabulary. Returns True if newly added."""
    if lemma not in data["vocabulary"]:
        data["vocabulary"].append(lemma)
        data["flashcard_progress"][lemma] = {
            "box": 1,
            "next_review": datetime.now().strftime("%Y-%m-%d"),
        }
        return True
    return False


def get_unlearned_words(data: dict) -> list[str]:
    """Return lemmas not yet in the user's vocabulary."""
    learned = set(data["vocabulary"])
    return [lemma for lemma in WORDS if lemma not in learned]


def get_due_flashcards(data: dict) -> list[str]:
    """Return lemmas due for review based on Leitner boxes."""
    today = datetime.now().strftime("%Y-%m-%d")
    due = []
    for lemma in data["vocabulary"]:
        progress = data["flashcard_progress"].get(lemma)
        if progress is None:
            due.append(lemma)
        elif progress["next_review"] <= today:
            due.append(lemma)
    return due


def review_flashcard(data: dict, lemma: str, easy: bool) -> None:
    """Update flashcard progress after review.

    easy=True  → advance to next box
    easy=False → reset to box 1
    """
    progress = data["flashcard_progress"].get(lemma, {"box": 1})
    if easy:
        new_box = min(progress["box"] + 1, 5)
    else:
        new_box = 1
    interval = BOX_INTERVALS[new_box]
    next_review = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")
    data["flashcard_progress"][lemma] = {
        "box": new_box,
        "next_review": next_review,
    }
