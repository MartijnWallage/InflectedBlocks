"""Sentence construction mode with interactive editing."""

from __future__ import annotations

from data import PROMPTS, WORDS, lookup_form, translate_english
from grammar import check_sentence, POS_TO_SYMBOL
from accentuation import check_accentuation
from ui import (
    console, display_prompt, display_errors, display_success,
    display_parse_tree, display_sentence_tokens, display_word_list_compact,
    display_translation_mismatch, display_accent_feedback, prompt_input, clear,
)


def _collect_english_words(roles: dict) -> list[str]:
    """Extract all English keywords from a roles dict."""
    words: list[str] = []
    if "verb" in roles:
        words.append(roles["verb"])
    for key in ("subject", "object", "dative"):
        np = roles.get(key)
        if isinstance(np, dict):
            if "noun" in np:
                words.append(np["noun"])
            if "adj" in np:
                words.append(np["adj"])
            part = np.get("participle")
            if isinstance(part, dict) and "verb" in part:
                words.append(part["verb"])
    pp = roles.get("pp")
    if isinstance(pp, dict):
        if "prep" in pp:
            words.append(pp["prep"])
        if "noun" in pp:
            words.append(pp["noun"])
    inf = roles.get("infinitive")
    if isinstance(inf, dict):
        if "verb" in inf:
            words.append(inf["verb"])
        inf_obj = inf.get("object")
        if isinstance(inf_obj, dict) and "noun" in inf_obj:
            words.append(inf_obj["noun"])
        inf_pp = inf.get("pp")
        if isinstance(inf_pp, dict):
            if "prep" in inf_pp:
                words.append(inf_pp["prep"])
            if "noun" in inf_pp:
                words.append(inf_pp["noun"])
    return words


def _needs_article(roles: dict) -> bool:
    """Check if any NP in roles is definite (requires the article ὁ)."""
    for key in ("subject", "object", "dative"):
        np = roles.get(key)
        if isinstance(np, dict) and not np.get("indef"):
            return True
    pp = roles.get("pp")
    if isinstance(pp, dict) and "noun" in pp:
        return True
    inf = roles.get("infinitive")
    if isinstance(inf, dict):
        inf_obj = inf.get("object")
        if isinstance(inf_obj, dict) and not inf_obj.get("indef"):
            return True
        inf_pp = inf.get("pp")
        if isinstance(inf_pp, dict) and "noun" in inf_pp:
            return True
    return False


def get_available_prompts(user_vocab: list[str]) -> list[dict]:
    """Return prompts for which the user knows all required lemmas."""
    vocab_set = set(user_vocab)
    available = []
    for prompt in PROMPTS:
        roles = prompt.get("roles")
        if not roles:
            continue
        ok = True
        for eng in _collect_english_words(roles):
            greek_lemmas = translate_english(eng)
            if not greek_lemmas or not any(g in vocab_set for g in greek_lemmas):
                ok = False
                break
        if ok and _needs_article(roles) and "ὁ" not in vocab_set:
            ok = False
        if ok:
            available.append(prompt)
    return available


def tokenize_input(text: str) -> list[str]:
    """Split input into tokens, handling punctuation."""
    # Simple whitespace split; strip trailing punctuation
    tokens = []
    for word in text.split():
        cleaned = word.strip(".,;:!?·")
        if cleaned:
            tokens.append(cleaned)
    return tokens


def _show_token_analysis(tokens: list[str]):
    """Show each token with its possible POS analyses."""
    token_analyses = []
    for token in tokens:
        analyses = lookup_form(token)
        readings = []
        for lemma, pos, feats in analyses:
            symbol = POS_TO_SYMBOL.get(pos)
            if symbol:
                readings.append((symbol, feats))
        token_analyses.append(readings)

    display_sentence_tokens(tokens, token_analyses)

    # Show details for each token
    for i, token in enumerate(tokens):
        analyses = lookup_form(token)
        if not analyses:
            console.print(f"  [red]'{token}' — not recognized[/red]")
        else:
            parts = []
            for lemma, pos, feats in analyses:
                feat_strs = []
                for k, v in feats.items():
                    if k != "lemma":
                        feat_strs.append(f"{v}")
                feat_str = ",".join(feat_strs) if feat_strs else ""
                parts.append(f"{pos}({lemma}) [{feat_str}]")
            console.print(f"  [dim]{token}: {' | '.join(parts)}[/dim]")


def _extract_np(node) -> dict:
    """Extract noun and adjective lemmas from an NP node."""
    result = {"has_article": False}
    for child in node.children:
        if child.symbol == "Art":
            result["has_article"] = True
        elif child.symbol == "N":
            result["noun"] = child.features.get("lemma")
        elif child.symbol == "Adj":
            result["adj"] = child.features.get("lemma")
        elif child.symbol == "Part":
            result["participle"] = {
                "lemma": child.features.get("lemma"),
                "tense": child.features.get("tense"),
                "voice": child.features.get("voice"),
            }
    # Bare noun (NP → N)
    if node.is_leaf() and node.symbol == "N":
        result["noun"] = node.features.get("lemma")
    return result


def _extract_pp(node) -> dict:
    """Extract prep lemma and NP contents from a PP node."""
    result = {}
    for child in node.children:
        if child.symbol == "Prep":
            result["prep"] = child.features.get("lemma")
        elif child.symbol == "NP":
            np_info = _extract_np(child)
            result["noun"] = np_info.get("noun")
            if "adj" in np_info:
                result["adj"] = np_info["adj"]
    return result


def _extract_infp(node) -> dict:
    """Extract verb, object, and PP from an InfP node."""
    result: dict = {}
    for child in node.children:
        if child.symbol == "V":
            result["verb"] = child.features.get("lemma")
            result["tense"] = child.features.get("tense")
            result["voice"] = child.features.get("voice")
        elif child.symbol == "NP":
            result["object"] = _extract_np(child)
        elif child.symbol == "PP":
            result["pp"] = _extract_pp(child)
    return result


def extract_roles(tree) -> dict:
    """Walk the parse tree and extract grammatical roles.

    Returns a dict with keys like "subject", "verb", "object", "pp".
    Roles are identified by case inflection, not by word order.
    For compound sentences (S Conj S), returns {"compound": True}.
    """
    if tree.symbol != "S":
        return {}

    # S → S Conj S
    if any(c.symbol == "Conj" for c in tree.children):
        return {"compound": True}

    roles: dict = {}

    # First pass: extract verb info (needed to determine object case)
    verb_obj_case = "acc"
    for child in tree.children:
        if child.symbol == "V":
            roles["verb"] = child.features.get("lemma")
            roles["tense"] = child.features.get("tense")
            roles["voice"] = child.features.get("voice")
            roles["person"] = child.features.get("person")
            roles["number"] = child.features.get("number")
            verb_obj_case = child.features.get("object_case", "acc")

    # Second pass: assign NP roles using verb's object case
    for child in tree.children:
        if child.symbol == "NP":
            np_case = child.features.get("case")
            if np_case == "nom":
                roles["subject"] = _extract_np(child)
            elif np_case == verb_obj_case:
                roles["object"] = _extract_np(child)
            elif np_case == "dat":
                roles["dative"] = _extract_np(child)
        elif child.symbol == "PP":
            roles["pp"] = _extract_pp(child)
        elif child.symbol == "InfP":
            roles["infinitive"] = _extract_infp(child)

    return roles


def _meaning(lemma: str) -> str:
    """Get the English meaning of a Greek lemma."""
    entry = WORDS.get(lemma)
    if entry:
        return entry.get("meaning", lemma)
    return lemma


def check_translation(actual: dict, expected: dict) -> tuple[bool, list[str]]:
    """Compare extracted roles against expected roles.

    Returns (match, list_of_mismatch_messages).
    """
    mismatches: list[str] = []

    if actual.get("compound"):
        mismatches.append("Expected a simple sentence, not a compound one")
        return False, mismatches

    # Check verb
    exp_verb = expected.get("verb")
    act_verb = actual.get("verb")
    if exp_verb and act_verb not in translate_english(exp_verb):
        mismatches.append(
            f'Expected verb "{exp_verb}", '
            f'got "{_meaning(act_verb)}" ({act_verb})' if act_verb
            else f'Expected verb "{exp_verb}", but none found'
        )

    # Check tense
    exp_tense = expected.get("tense")
    act_tense = actual.get("tense")
    if exp_tense and act_tense != exp_tense:
        tense_names = {
            "pres": "present", "impf": "imperfect",
            "fut": "future", "aor": "aorist",
        }
        mismatches.append(
            f'Expected {tense_names.get(exp_tense, exp_tense)} tense, '
            f'got {tense_names.get(act_tense, act_tense)}'
        )

    # Check voice
    exp_voice = expected.get("voice")
    act_voice = actual.get("voice")
    if exp_voice and act_voice != exp_voice:
        # Deponent verbs use middle forms but translate as active
        verb_lemma = actual.get("verb")
        is_deponent = WORDS.get(verb_lemma, {}).get("deponent", False)
        if is_deponent and exp_voice == "act" and act_voice == "mid":
            pass  # accept middle form for deponent verb
        else:
            voice_names = {"act": "active", "mid": "middle"}
            mismatches.append(
                f'Expected {voice_names.get(exp_voice, exp_voice)} voice, '
                f'got {voice_names.get(act_voice, act_voice)}'
            )

    # Check person
    exp_person = expected.get("person")
    act_person = actual.get("person")
    if exp_person and act_person != exp_person:
        person_names = {"1": "1st", "2": "2nd", "3": "3rd"}
        mismatches.append(
            f'Expected {person_names.get(exp_person, exp_person)} person, '
            f'got {person_names.get(act_person, act_person)}'
        )

    # Check number
    exp_number = expected.get("number")
    act_number = actual.get("number")
    if exp_number and act_number != exp_number:
        number_names = {"sg": "singular", "pl": "plural"}
        mismatches.append(
            f'Expected {number_names.get(exp_number, exp_number)} number, '
            f'got {number_names.get(act_number, act_number)}'
        )

    # Check subject
    exp_subj = expected.get("subject")
    act_subj = actual.get("subject")
    if exp_subj:
        if not act_subj:
            mismatches.append("Expected a subject noun phrase, but none found")
        else:
            _check_np_role("subject", exp_subj, act_subj, mismatches)
    elif act_subj:
        mismatches.append("Unexpected subject — the prompt doesn't have one")

    # Check object
    exp_obj = expected.get("object")
    act_obj = actual.get("object")
    if exp_obj:
        if not act_obj:
            mismatches.append("Expected an object noun phrase, but none found")
        else:
            _check_np_role("object", exp_obj, act_obj, mismatches)
    elif act_obj:
        mismatches.append("Unexpected object — the prompt doesn't have one")

    # Check dative
    exp_dat = expected.get("dative")
    act_dat = actual.get("dative")
    if exp_dat:
        if not act_dat:
            mismatches.append("Expected a dative noun phrase, but none found")
        else:
            _check_np_role("dative", exp_dat, act_dat, mismatches)
    elif act_dat:
        mismatches.append("Unexpected dative — the prompt doesn't have one")

    # Check PP
    exp_pp = expected.get("pp")
    act_pp = actual.get("pp")
    if exp_pp:
        if not act_pp:
            mismatches.append("Expected a prepositional phrase, but none found")
        else:
            exp_prep = exp_pp.get("prep")
            act_prep = act_pp.get("prep")
            if exp_prep and act_prep not in translate_english(exp_prep):
                mismatches.append(
                    f'Expected preposition "{exp_prep}", '
                    f'got "{_meaning(act_prep)}" ({act_prep})'
                )
            exp_pp_noun = exp_pp.get("noun")
            act_pp_noun = act_pp.get("noun")
            if exp_pp_noun and act_pp_noun not in translate_english(exp_pp_noun):
                mismatches.append(
                    f'In PP: expected noun "{exp_pp_noun}", '
                    f'got "{_meaning(act_pp_noun)}" ({act_pp_noun})'
                )
    elif act_pp:
        mismatches.append("Unexpected prepositional phrase — the prompt doesn't have one")

    # Check infinitive clause
    exp_inf = expected.get("infinitive")
    act_inf = actual.get("infinitive")
    if exp_inf:
        if not act_inf:
            mismatches.append("Expected an infinitive clause, but none found")
        else:
            exp_inf_verb = exp_inf.get("verb")
            act_inf_verb = act_inf.get("verb")
            if exp_inf_verb and act_inf_verb not in translate_english(exp_inf_verb):
                mismatches.append(
                    f'In infinitive: expected verb "{exp_inf_verb}", '
                    f'got "{_meaning(act_inf_verb)}" ({act_inf_verb})' if act_inf_verb
                    else f'In infinitive: expected verb "{exp_inf_verb}", but none found'
                )
            exp_inf_obj = exp_inf.get("object")
            act_inf_obj = act_inf.get("object")
            if exp_inf_obj:
                if not act_inf_obj:
                    mismatches.append("In infinitive: expected an object, but none found")
                else:
                    _check_np_role("infinitive object", exp_inf_obj, act_inf_obj, mismatches)
            elif act_inf_obj:
                mismatches.append("In infinitive: unexpected object")
            exp_inf_pp = exp_inf.get("pp")
            act_inf_pp = act_inf.get("pp")
            if exp_inf_pp:
                if not act_inf_pp:
                    mismatches.append("In infinitive: expected a PP, but none found")
                else:
                    exp_inf_prep = exp_inf_pp.get("prep")
                    act_inf_prep = act_inf_pp.get("prep")
                    if exp_inf_prep and act_inf_prep not in translate_english(exp_inf_prep):
                        mismatches.append(
                            f'In infinitive: expected preposition "{exp_inf_prep}", '
                            f'got "{_meaning(act_inf_prep)}" ({act_inf_prep})'
                        )
            elif act_inf_pp:
                mismatches.append("In infinitive: unexpected prepositional phrase")
    elif act_inf:
        mismatches.append("Unexpected infinitive clause — the prompt doesn't have one")

    return len(mismatches) == 0, mismatches


def _check_np_role(role: str, expected_np: dict, actual_np: dict,
                   mismatches: list[str]):
    """Compare an expected NP (noun + optional adj) against actual."""
    exp_noun = expected_np.get("noun")
    act_noun = actual_np.get("noun")
    if exp_noun and act_noun not in translate_english(exp_noun):
        mismatches.append(
            f'In {role}: expected "{exp_noun}", '
            f'got "{_meaning(act_noun)}" ({act_noun})'
        )

    exp_adj = expected_np.get("adj")
    act_adj = actual_np.get("adj")
    if exp_adj and act_adj not in translate_english(exp_adj):
        mismatches.append(
            f'In {role}: expected adjective "{exp_adj}", '
            f'got "{_meaning(act_adj)}" ({act_adj})' if act_adj
            else f'In {role}: expected adjective "{exp_adj}", but none found'
        )
    elif not exp_adj and act_adj:
        mismatches.append(
            f'In {role}: unexpected adjective "{_meaning(act_adj)}" ({act_adj})'
        )

    # Check participle
    exp_part = expected_np.get("participle")
    act_part = actual_np.get("participle")
    if exp_part:
        exp_part_verb = exp_part.get("verb")
        if not act_part:
            mismatches.append(
                f'In {role}: expected participle of "{exp_part_verb}", '
                f'but none found'
            )
        else:
            if act_part.get("lemma") not in translate_english(exp_part_verb):
                mismatches.append(
                    f'In {role}: expected participle of "{exp_part_verb}", '
                    f'got "{_meaning(act_part.get("lemma"))}" '
                    f'({act_part.get("lemma")})'
                )
    elif act_part:
        mismatches.append(
            f'In {role}: unexpected participle "{_meaning(act_part.get("lemma"))}" '
            f'({act_part.get("lemma")})'
        )

    # Check article: indefinite NPs must not have one, definite NPs must
    if expected_np.get("indef"):
        if actual_np.get("has_article"):
            mismatches.append(
                f'In {role}: indefinite noun phrase should not have an article in Greek'
            )
    else:
        if not actual_np.get("has_article"):
            mismatches.append(
                f'In {role}: definite noun phrase requires an article in Greek'
            )


def sentence_construction_loop(prompt: dict, user_vocab: list[str]) -> bool:
    """Interactive loop for building a sentence. Returns True if completed."""
    current_tokens: list[str] = []

    while True:
        clear()
        display_prompt(prompt["english"], prompt.get("hint", ""))

        if prompt.get("note"):
            console.print(f"  [italic yellow]Note: {prompt['note']}[/italic yellow]")

        console.print()

        # Show available vocabulary
        console.print("[dim]  Available words:[/dim]")
        display_word_list_compact(user_vocab)
        console.print()

        # Show current sentence
        if current_tokens:
            console.print("  [bold]Your sentence:[/bold]")
            _show_token_analysis(current_tokens)
            console.print()

            # Try to parse
            success, tree, errors = check_sentence(current_tokens)

            if success and tree:
                display_parse_tree(tree)
                expected = prompt.get("roles")
                if expected:
                    actual_roles = extract_roles(tree)
                    match, msgs = check_translation(actual_roles, expected)
                    if match:
                        accent_ok, accent_errors = check_accentuation(current_tokens)
                        if accent_ok:
                            display_success()
                            prompt_input("Press Enter to continue...")
                            return True
                        else:
                            display_accent_feedback(accent_errors)
                    else:
                        display_translation_mismatch(msgs)
                else:
                    accent_ok, accent_errors = check_accentuation(current_tokens)
                    if accent_ok:
                        display_success()
                        prompt_input("Press Enter to continue...")
                        return True
                    else:
                        display_accent_feedback(accent_errors)
            else:
                display_errors(errors)
        else:
            console.print("  [dim]Your sentence: (empty)[/dim]")

        console.print()
        console.print(
            "  [dim]Commands: type Greek words | "
            "'clear' to reset | 'back' to delete last | "
            "'quit' to exit[/dim]"
        )
        user_input = prompt_input("Greek> ").strip()

        if not user_input:
            continue
        elif user_input.lower() == "quit":
            return False
        elif user_input.lower() == "clear":
            current_tokens = []
        elif user_input.lower() == "back":
            if current_tokens:
                current_tokens.pop()
        else:
            new_tokens = tokenize_input(user_input)
            current_tokens.extend(new_tokens)


def run_sentence_mode(user_data: dict) -> None:
    """Run the sentence construction mode."""
    user_vocab = user_data.get("vocabulary", [])
    available = get_available_prompts(user_vocab)

    if not available:
        console.print(
            "\n[yellow]  You need to learn more words before building sentences![/yellow]"
        )
        console.print(
            "  [dim]Go to 'Study New Words' to expand your vocabulary.[/dim]\n"
        )
        prompt_input("Press Enter to return...")
        return

    console.print(f"\n  [bold]Sentence Builder[/bold] — {len(available)} prompts available\n")

    for i, prompt in enumerate(available):
        console.print(f"  [{i + 1}] {prompt['english']}")
    console.print(f"  [q] Return to menu")
    console.print()

    choice = prompt_input("Choose a sentence> ").strip()
    if choice.lower() == "q":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(available):
            completed = sentence_construction_loop(available[idx], user_vocab)
            if completed:
                user_data["sentences_completed"] = user_data.get("sentences_completed", 0) + 1
        else:
            console.print("[red]  Invalid choice.[/red]")
    except ValueError:
        console.print("[red]  Invalid choice.[/red]")
