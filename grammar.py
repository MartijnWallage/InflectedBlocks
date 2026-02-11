"""Context-free grammar with feature unification and chart parser."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import permutations as _permutations
from typing import Any

from data import lookup_form, WORDS


# ---------------------------------------------------------------------------
# Parse tree
# ---------------------------------------------------------------------------

class ParseNode:
    """A node in the parse tree."""

    def __init__(self, symbol: str, features: dict,
                 children: list | None = None, token: str | None = None):
        self.symbol = symbol
        self.features = features
        self.children = children or []
        self.token = token

    def is_leaf(self) -> bool:
        return self.token is not None

    def __repr__(self):
        if self.is_leaf():
            return f"{self.symbol}({self.token})"
        child_str = " ".join(repr(c) for c in self.children)
        return f"{self.symbol}[{child_str}]"


# Map POS tags to grammar symbols
POS_TO_SYMBOL = {
    "article": "Art",
    "noun": "N",
    "verb": "V",
    "adjective": "Adj",
    "preposition": "Prep",
    "conjunction": "Conj",
    "participle": "Part",
}

TERMINALS = {"Art", "N", "V", "Adj", "Prep", "Conj", "Part"}


# ---------------------------------------------------------------------------
# Token analysis
# ---------------------------------------------------------------------------

def analyze_tokens(tokens: list[str]) -> list[list[tuple[str, dict]]]:
    """For each token, return all possible (grammar_symbol, features) readings."""
    result = []
    for token in tokens:
        analyses = lookup_form(token)
        readings = []
        for lemma, pos, feats in analyses:
            symbol = POS_TO_SYMBOL.get(pos)
            if symbol:
                f = dict(feats)
                f["lemma"] = lemma
                readings.append((symbol, f))
        result.append(readings)
    return result


# ---------------------------------------------------------------------------
# Chart-based parser with feature unification
# ---------------------------------------------------------------------------

# Each rule: (lhs, rhs_symbols, constraint_fn)
# constraint_fn takes a list of feature dicts (one per rhs symbol) and returns
# the lhs features if constraints pass, or None if they fail.

def _agree(sym_feats: list[dict], indices: list[int], keys: list[str]) -> bool:
    """Check that the given feature keys agree across the given symbol indices."""
    for key in keys:
        vals = set()
        for i in indices:
            if i < len(sym_feats):
                v = sym_feats[i].get(key)
                if v is not None:
                    vals.add(v)
        if len(vals) > 1:
            return False
    return True


def _get_feat(sym_feats: list[dict], idx: int, key: str) -> str | None:
    """Get a feature value from a symbol's features."""
    if idx < len(sym_feats):
        return sym_feats[idx].get(key)
    return None


# ---------------------------------------------------------------------------
# Flat sentence rules — Greek has free word order at the clause level.
# Grammatical roles (subject, object) are determined by case inflections,
# not by position.  We generate S rules for every permutation of the
# clause-level constituents (NP-nom, V, NP-acc, PP).
# ---------------------------------------------------------------------------

def _make_flat_s_constraint(roles: list[str]):
    """Return a constraint function for a flat S rule.

    *roles* maps each RHS position to its grammatical role:
    "subj" (NP-nom), "verb" (V), "obj" (NP-acc), "pp" (PP).
    """
    v_idx = roles.index("verb")
    subj_idx = roles.index("subj") if "subj" in roles else None

    def constraint(feats):
        for idx, role in enumerate(roles):
            if role == "subj" and _get_feat(feats, idx, "case") != "nom":
                return None
            if role == "obj" and _get_feat(feats, idx, "case") != "acc":
                return None

        if subj_idx is not None:
            if not _agree(feats, [subj_idx, v_idx], ["number"]):
                return None
            vp_person = _get_feat(feats, v_idx, "person")
            if vp_person and vp_person != "3":
                return None

        result = {}
        num = _get_feat(feats, v_idx, "number")
        person = _get_feat(feats, v_idx, "person")
        if num:
            result["number"] = num
        if person:
            result["person"] = person
        return result

    return constraint


def _add_sentence_rules(rules: list):
    """Add flat S → … rules for every word-order permutation."""
    patterns = [
        # pro-drop
        [("V", "verb")],
        [("V", "verb"), ("NP", "obj")],
        [("V", "verb"), ("PP", "pp")],
        [("V", "verb"), ("NP", "obj"), ("PP", "pp")],
        # with overt subject
        [("NP", "subj"), ("V", "verb")],
        [("NP", "subj"), ("V", "verb"), ("NP", "obj")],
        [("NP", "subj"), ("V", "verb"), ("PP", "pp")],
        [("NP", "subj"), ("V", "verb"), ("NP", "obj"), ("PP", "pp")],
    ]
    for pattern in patterns:
        seen: set[tuple] = set()
        for perm in _permutations(range(len(pattern))):
            rhs = [pattern[i][0] for i in perm]
            perm_roles = [pattern[i][1] for i in perm]
            key = (tuple(rhs), tuple(perm_roles))
            if key in seen:
                continue
            seen.add(key)
            rules.append(("S", rhs, _make_flat_s_constraint(perm_roles)))


# Rule definitions as (lhs, rhs, constraint_function)
def _make_rules():
    rules = []

    # -- NP rules (word order within NP is fixed in Greek) ---------------

    # NP → Art N  (article + noun, must agree)
    def np_art_n(feats):
        if not _agree(feats, [0, 1], ["case", "number", "gender"]):
            return None
        return {
            "case": _get_feat(feats, 0, "case") or _get_feat(feats, 1, "case"),
            "number": _get_feat(feats, 0, "number") or _get_feat(feats, 1, "number"),
            "gender": _get_feat(feats, 0, "gender") or _get_feat(feats, 1, "gender"),
        }
    rules.append(("NP", ["Art", "N"], np_art_n))

    # NP → Art Adj N  (article + adjective + noun, all agree)
    def np_art_adj_n(feats):
        if not _agree(feats, [0, 1, 2], ["case", "number", "gender"]):
            return None
        return {
            "case": _get_feat(feats, 0, "case") or _get_feat(feats, 2, "case"),
            "number": _get_feat(feats, 0, "number") or _get_feat(feats, 2, "number"),
            "gender": _get_feat(feats, 0, "gender") or _get_feat(feats, 2, "gender"),
        }
    rules.append(("NP", ["Art", "Adj", "N"], np_art_adj_n))

    # NP → Art N Adj  (article + noun + adjective, all agree)
    def np_art_n_adj(feats):
        if not _agree(feats, [0, 1, 2], ["case", "number", "gender"]):
            return None
        return {
            "case": _get_feat(feats, 0, "case") or _get_feat(feats, 1, "case"),
            "number": _get_feat(feats, 0, "number") or _get_feat(feats, 1, "number"),
            "gender": _get_feat(feats, 0, "gender") or _get_feat(feats, 1, "gender"),
        }
    rules.append(("NP", ["Art", "N", "Adj"], np_art_n_adj))

    # NP → Art Part N  (article + participle + noun, all agree)
    def np_art_part_n(feats):
        if not _agree(feats, [0, 1, 2], ["case", "number", "gender"]):
            return None
        return {
            "case": _get_feat(feats, 0, "case") or _get_feat(feats, 2, "case"),
            "number": _get_feat(feats, 0, "number") or _get_feat(feats, 2, "number"),
            "gender": _get_feat(feats, 0, "gender") or _get_feat(feats, 2, "gender"),
        }
    rules.append(("NP", ["Art", "Part", "N"], np_art_part_n))

    # NP → Art N Part  (article + noun + participle, all agree)
    def np_art_n_part(feats):
        if not _agree(feats, [0, 1, 2], ["case", "number", "gender"]):
            return None
        return {
            "case": _get_feat(feats, 0, "case") or _get_feat(feats, 1, "case"),
            "number": _get_feat(feats, 0, "number") or _get_feat(feats, 1, "number"),
            "gender": _get_feat(feats, 0, "gender") or _get_feat(feats, 1, "gender"),
        }
    rules.append(("NP", ["Art", "N", "Part"], np_art_n_part))

    # NP → N  (bare noun)
    def np_n(feats):
        return {
            "case": _get_feat(feats, 0, "case"),
            "number": _get_feat(feats, 0, "number"),
            "gender": _get_feat(feats, 0, "gender"),
        }
    rules.append(("NP", ["N"], np_n))

    # -- PP rule (preposition precedes NP in Greek) ----------------------

    # PP → Prep NP  (preposition governs NP case)
    def pp_prep_np(feats):
        gov = _get_feat(feats, 0, "governs")
        np_case = _get_feat(feats, 1, "case")
        if gov and np_case and gov != np_case:
            return None
        return {}
    rules.append(("PP", ["Prep", "NP"], pp_prep_np))

    # -- Flat sentence rules (all word-order permutations) ---------------

    _add_sentence_rules(rules)

    # S → S Conj S
    def s_conj_s(feats):
        return {}
    rules.append(("S", ["S", "Conj", "S"], s_conj_s))

    return rules


RULES = _make_rules()


class ChartParser:
    """CYK-style chart parser extended for arbitrary rule lengths."""

    def __init__(self):
        self.rules = RULES

    def parse(self, tokens: list[str]) -> tuple[bool, ParseNode | None, list[str]]:
        n = len(tokens)
        if n == 0:
            return False, None, ["Empty input"]

        token_readings = analyze_tokens(tokens)

        # Check for unrecognized tokens
        for i, readings in enumerate(token_readings):
            if not readings:
                return False, None, [f"Unknown word: '{tokens[i]}'"]

        # Chart: chart[i][j] = list of (symbol, features, ParseNode)
        # for spans from token i to token j (exclusive)
        chart: list[list[list[tuple[str, dict, ParseNode]]]] = [
            [[] for _ in range(n + 1)] for _ in range(n + 1)
        ]

        # Fill in terminals (length-1 spans)
        for i in range(n):
            for symbol, feats in token_readings[i]:
                node = ParseNode(symbol, feats, token=tokens[i])
                chart[i][i + 1].append((symbol, feats, node))

        # Fill in longer spans
        changed = True
        while changed:
            changed = False
            for length in range(1, n + 1):
                for start in range(n - length + 1):
                    end = start + length
                    for lhs, rhs, constraint_fn in self.rules:
                        # Try all ways to split [start, end) according to rhs
                        for split_result in self._splits(chart, rhs, start, end):
                            # split_result: list of (symbol, features, node) for each rhs symbol
                            feat_list = [item[1] for item in split_result]
                            lhs_feats = constraint_fn(feat_list)
                            if lhs_feats is not None:
                                children = [item[2] for item in split_result]
                                # Clean up None values in features
                                clean_feats = {k: v for k, v in lhs_feats.items() if v is not None}
                                new_node = ParseNode(lhs, clean_feats, children)
                                # Check if we already have this
                                key = (lhs, tuple(sorted(clean_feats.items())))
                                existing = [(s, tuple(sorted(f.items())))
                                            for s, f, _ in chart[start][end]]
                                if key not in existing:
                                    chart[start][end].append((lhs, clean_feats, new_node))
                                    changed = True

        # Look for S spanning the whole input
        for symbol, feats, node in chart[0][n]:
            if symbol == "S":
                return True, node, []

        # No complete parse - diagnose errors
        errors = self._diagnose(chart, tokens, token_readings, n)
        return False, None, errors

    def _splits(self, chart, rhs: list[str], start: int, end: int):
        """Generate all ways to split [start, end) into len(rhs) contiguous spans,
        each matching the corresponding rhs symbol."""
        if len(rhs) == 0:
            if start == end:
                yield []
            return

        if len(rhs) == 1:
            sym = rhs[0]
            for s, f, node in chart[start][end]:
                if s == sym:
                    yield [(s, f, node)]
            return

        # Try all split points for the first symbol
        sym = rhs[0]
        for mid in range(start + 1, end):
            for s, f, node in chart[start][mid]:
                if s == sym:
                    for rest in self._splits(chart, rhs[1:], mid, end):
                        yield [(s, f, node)] + rest

    def _diagnose(self, chart, tokens, token_readings, n) -> list[str]:
        """Produce error messages from partial parses."""
        errors = []

        # Check for agreement errors between adjacent tokens
        self._check_agreement_errors(tokens, token_readings, errors)

        # Check if there is a verb anywhere
        has_verb = any(
            s == "V"
            for i in range(n)
            for s, _, _ in chart[i][i + 1]
        )
        if not has_verb:
            has_np = any(
                s == "NP"
                for i in range(n)
                for j in range(i + 1, n + 1)
                for s, _, _ in chart[i][j]
            )
            if has_np:
                errors.append(
                    "Found a noun phrase but no verb. "
                    "Add a verb to complete the sentence."
                )
            elif not errors:
                errors.append("No verb found in the sentence.")
            return errors

        # Check for preposition case errors
        for i in range(n):
            prep_readings = [f for s, f in token_readings[i] if s == "Prep"]
            if prep_readings:
                gov = prep_readings[0].get("governs")
                if gov and i + 1 < n:
                    # Look for NP starting at i+1
                    found_np = False
                    for end in range(i + 2, n + 1):
                        for sym, feats, _ in chart[i + 1][end]:
                            if sym == "NP":
                                found_np = True
                                np_case = feats.get("case")
                                if np_case and np_case != gov:
                                    errors.append(
                                        f"Preposition '{tokens[i]}' governs {gov} case "
                                        f"but the NP is {np_case}"
                                    )
                    if not found_np:
                        errors.append(
                            f"Preposition '{tokens[i]}' needs a noun phrase after it"
                        )

        if not errors:
            errors.append(
                "Sentence structure not recognized. "
                "Check case forms and agreement."
            )
        return errors

    def _check_agreement_errors(self, tokens, token_readings, errors):
        """Check for specific agreement problems."""
        n = len(tokens)
        for i in range(n - 1):
            arts = [(s, f) for s, f in token_readings[i] if s == "Art"]
            nouns = [(s, f) for s, f in token_readings[i + 1] if s == "N"]

            if arts and nouns:
                any_agrees = False
                for _, af in arts:
                    for _, nf in nouns:
                        if (af.get("case") == nf.get("case") and
                                af.get("number") == nf.get("number") and
                                af.get("gender") == nf.get("gender")):
                            any_agrees = True
                            break
                    if any_agrees:
                        break
                if not any_agrees:
                    for _, af in arts:
                        for _, nf in nouns:
                            mismatches = []
                            for feat in ("case", "number", "gender"):
                                if af.get(feat) and nf.get(feat) and af[feat] != nf[feat]:
                                    mismatches.append(
                                        f"{feat}: article is {af[feat]}, "
                                        f"noun is {nf[feat]}"
                                    )
                            if mismatches:
                                errors.append(
                                    f"Agreement error between '{tokens[i]}' and "
                                    f"'{tokens[i + 1]}': {'; '.join(mismatches)}"
                                )
                                return

            adjs = [(s, f) for s, f in token_readings[i + 1] if s == "Adj"]
            if arts and adjs:
                any_agrees = False
                for _, af in arts:
                    for _, jf in adjs:
                        if (af.get("case") == jf.get("case") and
                                af.get("number") == jf.get("number") and
                                af.get("gender") == jf.get("gender")):
                            any_agrees = True
                            break
                    if any_agrees:
                        break
                if not any_agrees:
                    for _, af in arts:
                        for _, jf in adjs:
                            mismatches = []
                            for feat in ("case", "number", "gender"):
                                if af.get(feat) and jf.get(feat) and af[feat] != jf[feat]:
                                    mismatches.append(
                                        f"{feat}: article is {af[feat]}, "
                                        f"adjective is {jf[feat]}"
                                    )
                            if mismatches:
                                errors.append(
                                    f"Agreement error between '{tokens[i]}' and "
                                    f"'{tokens[i + 1]}': {'; '.join(mismatches)}"
                                )
                                return

        # Subject-verb number and person agreement
        first_nom_noun = None
        first_verb = None
        first_verb_feats = None
        for i in range(n):
            for s, f in token_readings[i]:
                if s == "N" and f.get("case") == "nom" and first_nom_noun is None:
                    first_nom_noun = (f.get("number"), tokens[i])
                if s == "V" and first_verb is None:
                    first_verb = (f.get("number"), tokens[i])
                    first_verb_feats = f
        if first_nom_noun and first_verb:
            if (first_nom_noun[0] and first_verb[0] and
                    first_nom_noun[0] != first_verb[0]):
                errors.append(
                    f"Number disagreement: subject '{first_nom_noun[1]}' is "
                    f"{first_nom_noun[0]} but verb '{first_verb[1]}' is "
                    f"{first_verb[0]}"
                )
            verb_person = first_verb_feats.get("person")
            if verb_person and verb_person != "3":
                person_names = {"1": "1st", "2": "2nd", "3": "3rd"}
                errors.append(
                    f"Person disagreement: noun subject '{first_nom_noun[1]}' is "
                    f"3rd person but verb '{first_verb[1]}' is "
                    f"{person_names.get(verb_person, verb_person)} person"
                )


def check_sentence(tokens: list[str]) -> tuple[bool, ParseNode | None, list[str]]:
    """Parse a token list and return (success, tree, errors)."""
    parser = ChartParser()
    return parser.parse(tokens)
