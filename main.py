"""Entry point for the Ancient Greek Learning App."""

from __future__ import annotations

import random

from data import WORDS
from vocabulary import (
    load_user_data, save_user_data, add_to_vocabulary,
    get_unlearned_words, get_due_flashcards, review_flashcard,
)
from sentences import run_sentence_mode
from ui import (
    console, clear, display_main_menu, display_flashcard,
    display_vocabulary_list, prompt_input,
)


def study_new_words(data: dict) -> None:
    """Present unlearned words as flashcards for the user to study."""
    unlearned = get_unlearned_words(data)
    if not unlearned:
        console.print("\n  [green]You've learned all available words![/green]\n")
        prompt_input("Press Enter to return...")
        return

    console.print(f"\n  [bold]Study New Words[/bold] — {len(unlearned)} words remaining\n")

    # Present up to 5 words at a time
    batch = unlearned[:5]
    for lemma in batch:
        clear()
        console.print(f"\n  [dim]New word ({unlearned.index(lemma) + 1}/{len(unlearned)})[/dim]\n")

        # Show front of card
        display_flashcard(lemma, revealed=False)
        prompt_input("Press Enter to reveal...")

        clear()
        console.print()

        # Show back of card
        display_flashcard(lemma, revealed=True)

        while True:
            choice = prompt_input("Your choice> ").strip()
            if choice == "1":
                add_to_vocabulary(data, lemma)
                review_flashcard(data, lemma, easy=True)
                save_user_data(data)
                console.print("  [green]Marked as easy. Added to vocabulary.[/green]")
                break
            elif choice == "2":
                add_to_vocabulary(data, lemma)
                review_flashcard(data, lemma, easy=False)
                save_user_data(data)
                console.print("  [yellow]Marked as hard. Will review soon.[/yellow]")
                break
            elif choice == "3":
                added = add_to_vocabulary(data, lemma)
                save_user_data(data)
                if added:
                    console.print("  [cyan]Added to vocabulary![/cyan]")
                else:
                    console.print("  [dim]Already in vocabulary.[/dim]")
                break
            else:
                console.print("  [dim]Press 1 (easy), 2 (hard), or 3 (add)[/dim]")

        prompt_input("Press Enter for next word...")


def review_flashcards(data: dict) -> None:
    """Review due flashcards."""
    due = get_due_flashcards(data)
    if not due:
        console.print("\n  [green]No flashcards due for review![/green]")
        console.print("  [dim]Come back later or study new words.[/dim]\n")
        prompt_input("Press Enter to return...")
        return

    random.shuffle(due)
    console.print(f"\n  [bold]Flashcard Review[/bold] — {len(due)} cards due\n")

    for i, lemma in enumerate(due):
        clear()
        console.print(f"\n  [dim]Card {i + 1}/{len(due)}[/dim]\n")

        display_flashcard(lemma, revealed=False)
        prompt_input("Press Enter to reveal...")

        clear()
        console.print()
        display_flashcard(lemma, revealed=True)

        while True:
            choice = prompt_input("Your choice (1=easy, 2=hard)> ").strip()
            if choice == "1":
                review_flashcard(data, lemma, easy=True)
                save_user_data(data)
                console.print("  [green]Nice! Moving to next box.[/green]")
                break
            elif choice == "2":
                review_flashcard(data, lemma, easy=False)
                save_user_data(data)
                console.print("  [yellow]Reset to box 1. You'll see it again soon.[/yellow]")
                break
            else:
                console.print("  [dim]Press 1 (easy) or 2 (hard)[/dim]")

        if i < len(due) - 1:
            prompt_input("Press Enter for next card...")

    console.print(f"\n  [bold green]Review complete! {len(due)} cards reviewed.[/bold green]\n")
    prompt_input("Press Enter to return...")


def view_vocabulary(data: dict) -> None:
    """Display the user's learned vocabulary."""
    console.print()
    display_vocabulary_list(data.get("vocabulary", []))
    completed = data.get("sentences_completed", 0)
    if completed:
        console.print(f"\n  [dim]Sentences completed: {completed}[/dim]")
    console.print()
    prompt_input("Press Enter to return...")


def main():
    """Main application loop."""
    data = load_user_data()

    while True:
        clear()
        console.print()
        display_main_menu()
        console.print()

        choice = prompt_input("Choose> ").strip().lower()

        match choice:
            case "1":
                study_new_words(data)
            case "2":
                review_flashcards(data)
            case "3":
                run_sentence_mode(data)
                save_user_data(data)
            case "4":
                view_vocabulary(data)
            case "q" | "quit":
                save_user_data(data)
                console.print("\n  [bold]Χαῖρε![/bold] (Farewell!)\n")
                break
            case _:
                console.print("  [red]Invalid choice.[/red]")
                prompt_input("Press Enter...")


if __name__ == "__main__":
    main()
