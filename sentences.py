"""Sentence construction mode with interactive editing."""

from __future__ import annotations

from data import PROMPTS, WORDS, lookup_form
from grammar import check_sentence, POS_TO_SYMBOL
from ui import (
    console, display_prompt, display_errors, display_success,
    display_parse_tree, display_sentence_tokens, display_word_list_compact,
    prompt_input, clear,
)


def get_available_prompts(user_vocab: list[str]) -> list[dict]:
    """Return prompts for which the user knows all required lemmas."""
    vocab_set = set(user_vocab)
    available = []
    for prompt in PROMPTS:
        if all(lemma in vocab_set for lemma in prompt["required_lemmas"]):
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
                display_success()
                prompt_input("Press Enter to continue...")
                return True
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
