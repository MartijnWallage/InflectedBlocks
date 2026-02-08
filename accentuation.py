"""Accentuation utilities for Attic Greek sentential accent rules.

In Attic Greek prose, oxytone words (acute on the ultima) change their
acute to a grave when followed by another word in the same clause.
The database stores all forms in citation form (with acute), so this
module provides:
  - normalize_graves: convert graves back to acutes for dictionary lookup
  - acute_to_grave_on_ultima: apply the sentential grave rule
  - check_accentuation: check a list of tokens for correct sentential accents
"""

from __future__ import annotations

import unicodedata

COMBINING_ACUTE = "\u0301"
COMBINING_GRAVE = "\u0300"
GREEK_VOWELS = set("αεηιουωάέήίόύώὰὲὴὶὸὺὼ"
                   "ΑΕΗΙΟΥΩΆΈΉΊΌΎΏ")


def normalize_graves(word: str) -> str:
    """Replace all combining graves with combining acutes.

    NFD-decompose, swap U+0300 → U+0301, NFC-recompose.
    This converts sentential grave forms back to citation (acute) forms
    for dictionary lookup.
    """
    decomposed = unicodedata.normalize("NFD", word)
    replaced = decomposed.replace(COMBINING_GRAVE, COMBINING_ACUTE)
    return unicodedata.normalize("NFC", replaced)


def acute_to_grave_on_ultima(word: str) -> str:
    """If the word has an acute on its ultima, replace it with a grave.

    NFD-decompose, find the *last* combining acute. If no Greek vowel
    follows that acute, it sits on the ultima → replace with grave.
    Returns the word unchanged if no acute is on the ultima.
    """
    decomposed = unicodedata.normalize("NFD", word)
    # Find the last combining acute
    last_acute = decomposed.rfind(COMBINING_ACUTE)
    if last_acute == -1:
        return word  # no acute at all

    # Check whether any vowel follows the last acute
    after = decomposed[last_acute + 1:]
    has_vowel_after = any(ch in GREEK_VOWELS for ch in after)

    if has_vowel_after:
        # Acute is not on the ultima – leave unchanged
        return word

    # Acute is on the ultima – replace with grave
    result = decomposed[:last_acute] + COMBINING_GRAVE + decomposed[last_acute + 1:]
    return unicodedata.normalize("NFC", result)


def check_accentuation(user_tokens: list[str]) -> tuple[bool, list[str]]:
    """Check sentential accentuation of a list of tokens.

    For each non-final token, the expected form applies the grave rule
    (acute on ultima becomes grave). The final token keeps its citation
    accent.

    Returns (all_correct, error_messages).
    """
    errors = []
    for i, token in enumerate(user_tokens):
        # Get citation form by normalizing graves → acutes
        citation = normalize_graves(token)

        if i < len(user_tokens) - 1:
            # Non-final: apply grave rule
            expected = acute_to_grave_on_ultima(citation)
        else:
            # Final token: keep citation accent (acute)
            expected = citation

        if token != expected:
            if expected != citation:
                errors.append(
                    f"'{citation}' → '{expected}' "
                    f"(acute becomes grave before the next word)"
                )
            else:
                errors.append(
                    f"'{token}' → '{expected}' "
                    f"(final word keeps its acute accent)"
                )

    return (len(errors) == 0, errors)
