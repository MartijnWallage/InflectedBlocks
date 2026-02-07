"""Rich-based terminal UI for the Greek learning app."""

from __future__ import annotations

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box

from data import WORDS
from grammar import ParseNode

console = Console()

# Color scheme
COLORS = {
    "Art": "cyan",
    "N": "green",
    "V": "magenta",
    "Adj": "yellow",
    "Prep": "blue",
    "Conj": "white",
    "NP": "green",
    "VP": "magenta",
    "PP": "blue",
    "S": "white",
}

CASE_ABBREV = {"nom": "nom", "gen": "gen", "dat": "dat", "acc": "acc", "voc": "voc"}
GENDER_ABBREV = {"masculine": "m", "feminine": "f", "neuter": "n",
                 "masc": "m", "fem": "f", "neut": "n"}
NUMBER_ABBREV = {"sg": "sg", "pl": "pl"}


def clear():
    """Clear the console."""
    console.clear()


def display_main_menu():
    """Display the main menu."""
    menu = Text()
    menu.append("  [1] ", style="bold cyan")
    menu.append("Study New Words\n")
    menu.append("  [2] ", style="bold cyan")
    menu.append("Review Flashcards\n")
    menu.append("  [3] ", style="bold cyan")
    menu.append("Build Sentences\n")
    menu.append("  [4] ", style="bold cyan")
    menu.append("View Vocabulary\n")
    menu.append("  [q] ", style="bold red")
    menu.append("Quit")

    panel = Panel(
        menu,
        title="[bold]ΜΑΘΕ ΕΛΛΗΝΙΚΑ[/bold]",
        subtitle="Learn Ancient Greek",
        border_style="bright_blue",
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(panel)


def display_flashcard(lemma: str, revealed: bool = False):
    """Display a flashcard for a word."""
    entry = WORDS.get(lemma)
    if not entry:
        console.print(f"[red]Word not found: {lemma}[/red]")
        return

    pos = entry["pos"]
    meaning = entry["meaning"]

    # Header info
    header = Text()
    header.append(f"  {lemma}\n", style="bold bright_white")

    if pos == "noun":
        header.append(f"  {pos}, {entry.get('gender', '')}, "
                      f"{entry.get('declension', '')}{'st' if entry.get('declension') == 1 else 'nd'} declension",
                      style="dim")
    elif pos == "verb":
        header.append(f"  {pos}, {entry.get('conjugation', '')}",
                      style="dim")
    elif pos == "adjective":
        header.append(f"  {pos}", style="dim")
    else:
        header.append(f"  {pos}", style="dim")

    if not revealed:
        content = Text()
        content.append(str(header))
        content.append("\n\n  [Press Enter to reveal]", style="italic dim")
        panel = Panel(
            content,
            border_style="yellow",
            box=box.DOUBLE,
            padding=(1, 1),
        )
        console.print(panel)
    else:
        header_text = Text()
        header_text.append(str(header))
        header_text.append(f'\n\n  "{meaning}"', style="bold green")

        # Build forms table
        forms = entry.get("forms", {})
        cases = ["nom", "gen", "dat", "acc"]

        if pos == "noun":
            tbl = Table(show_header=False, box=None, padding=(0, 1),
                        pad_edge=False)
            tbl.add_column(style="dim")
            tbl.add_column(style="bright_white")
            for number in ("sg", "pl"):
                if number == "pl":
                    tbl.add_row("", "")
                for case in cases:
                    key = f"{case}_{number}"
                    if key in forms:
                        tbl.add_row(f"{case}.{number}", forms[key])

        elif pos == "verb":
            tbl = Table(show_header=False, box=None, padding=(0, 1),
                        pad_edge=False)
            tbl.add_column(style="dim")
            tbl.add_column(style="bright_white")
            for number in ("sg", "pl"):
                if number == "pl":
                    tbl.add_row("", "")
                for person in ("1", "2", "3"):
                    key = f"pres_act_ind_{person}{number}"
                    if key in forms:
                        tbl.add_row(f"pres.act.{person}{number}",
                                    forms[key])

        elif pos in ("article", "adjective"):
            tbl = Table(show_header=False, box=None, padding=(0, 1),
                        pad_edge=False)
            tbl.add_column(style="dim")
            tbl.add_column(style="bright_white")
            tbl.add_column(style="bright_white")
            tbl.add_column(style="bright_white")
            for number in ("sg", "pl"):
                if number == "pl":
                    tbl.add_row("", "", "", "")
                for case in cases:
                    masc = forms.get(f"{case}_{number}_masc", "")
                    fem = forms.get(f"{case}_{number}_fem", "")
                    neut = forms.get(f"{case}_{number}_neut", "")
                    if masc or fem or neut:
                        tbl.add_row(f"{case}.{number}", masc, fem, neut)
        else:
            tbl = None

        # Rating buttons
        rating = Text()
        rating.append("  [1] ", style="bold green")
        rating.append("Easy   ")
        rating.append("[2] ", style="bold red")
        rating.append("Hard   ")
        rating.append("[3] ", style="bold cyan")
        rating.append("Add to vocabulary")

        parts = [header_text, Text("")]
        if tbl is not None:
            parts.append(tbl)
        parts.append(Text(""))
        parts.append(rating)

        panel = Panel(
            Group(*parts),
            border_style="green",
            box=box.DOUBLE,
            padding=(1, 1),
        )
        console.print(panel)


def _format_features_short(features: dict) -> str:
    """Format features as a short string."""
    parts = []
    if "case" in features:
        parts.append(CASE_ABBREV.get(features["case"], features["case"]))
    if "number" in features:
        parts.append(NUMBER_ABBREV.get(features["number"], features["number"]))
    if "gender" in features:
        parts.append(GENDER_ABBREV.get(features["gender"], features["gender"]))
    if "person" in features:
        parts.append(f"{features['person']}p")
    if "tense" in features:
        parts.append(features["tense"])
    if "voice" in features:
        parts.append(features["voice"])
    return ",".join(parts)


def _build_tree_renderable(node: ParseNode):
    """Recursively build a Rich renderable for a parse tree node."""
    feat_str = _format_features_short(node.features)
    color = COLORS.get(node.symbol, "white")

    if node.is_leaf():
        label = node.symbol
        if feat_str:
            label += f" [{feat_str}]"
        return Panel(
            Text(node.token, style=f"bold {color}", justify="center"),
            title=label,
            border_style=color,
            box=box.ROUNDED,
            padding=(0, 1),
        )

    # Nonterminal: recursively build children
    child_renderables = [_build_tree_renderable(c) for c in node.children]

    label = node.symbol
    if feat_str:
        label += f"[{feat_str}]"

    return Panel(
        Columns(child_renderables, padding=(0, 1)),
        title=label,
        border_style=color,
        box=box.ROUNDED,
    )


def display_parse_tree(tree: ParseNode, indent: int = 0):
    """Display a parse tree with colored nested boxes."""
    if tree is None:
        return

    renderable = _build_tree_renderable(tree)
    # Use heavy box for the outermost S node
    if not tree.is_leaf() and tree.symbol == "S":
        feat_str = _format_features_short(tree.features)
        color = COLORS.get(tree.symbol, "white")
        label = tree.symbol
        if feat_str:
            label += f"[{feat_str}]"
        child_renderables = [_build_tree_renderable(c) for c in tree.children]
        renderable = Panel(
            Columns(child_renderables, padding=(0, 1)),
            title=f"[bold]{label}[/bold]",
            border_style=color,
            box=box.HEAVY,
        )
    console.print(renderable)


def display_sentence_tokens(tokens: list[str], token_analyses: list[list[tuple[str, dict]]]):
    """Display tokens with their POS colors (before full parse)."""
    text = Text()
    for i, token in enumerate(tokens):
        analyses = token_analyses[i] if i < len(token_analyses) else []
        if analyses:
            symbol = analyses[0][0]
            color = COLORS.get(symbol, "white")
        else:
            color = "red"
        if i > 0:
            text.append(" ")
        text.append(token, style=f"bold {color}")
    console.print(text)


def display_errors(errors: list[str]):
    """Display error messages."""
    for err in errors:
        console.print(f"  [red]✗[/red] {err}")


def display_success(message: str = "Correct! Well done!"):
    """Display a success message."""
    console.print(f"\n  [bold green]✓ {message}[/bold green]\n")


def display_translation_mismatch(mismatches: list[str]):
    """Display grammar-OK but wrong-translation feedback."""
    console.print("\n  [bold green]✓ Grammatically correct![/bold green]")
    console.print("  [yellow]But not quite the right translation:[/yellow]")
    for msg in mismatches:
        console.print(f"  [yellow]⚠ {msg}[/yellow]")
    console.print()


def display_prompt(english: str, hint: str = ""):
    """Display a sentence construction prompt."""
    content = Text()
    content.append(f"  {english}", style="bold bright_white")
    if hint:
        content.append(f"\n  Hint: {hint}", style="italic dim")
    panel = Panel(
        content,
        title="Translate",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 1),
    )
    console.print(panel)


def display_vocabulary_list(vocabulary: list[str]):
    """Display the user's learned vocabulary as a table."""
    if not vocabulary:
        console.print("[dim]  No words learned yet. Try [bold]Study New Words[/bold]![/dim]")
        return

    table = Table(
        title="Your Vocabulary",
        box=box.ROUNDED,
        border_style="bright_blue",
        show_lines=True,
    )
    table.add_column("Greek", style="bold bright_white", justify="center")
    table.add_column("POS", style="dim")
    table.add_column("Meaning", style="green")
    table.add_column("Box", style="cyan", justify="center")

    for lemma in vocabulary:
        entry = WORDS.get(lemma)
        if entry:
            table.add_row(
                lemma,
                entry["pos"],
                entry["meaning"],
                "",
            )
    console.print(table)


def display_word_list_compact(lemmas: list[str]):
    """Show a compact list of available words."""
    panels = []
    for lemma in lemmas:
        entry = WORDS.get(lemma)
        if entry:
            color = COLORS.get(
                {"noun": "N", "verb": "V", "adjective": "Adj",
                 "article": "Art", "preposition": "Prep",
                 "conjunction": "Conj"}.get(entry["pos"], ""),
                "white"
            )
            panels.append(
                Text(f"{lemma} ", style=f"{color}")
            )
    if panels:
        console.print(Columns(panels, padding=(0, 1)))


def prompt_input(prompt_text: str = "> ") -> str:
    """Get user input with a styled prompt."""
    return console.input(f"[bold cyan]{prompt_text}[/bold cyan]")
