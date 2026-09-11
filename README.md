# InflectedBlocks

A language-learning application designed for inflected languages.

InflectedBlocks is currently focused on Ancient Greek. It combines vocabulary
learning with grammar and sentence construction, allowing the learner to
practise not only individual word forms but also their use in complete
sentences.

## Features

### Vocabulary learning

- Add and study Greek vocabulary through flashcards.
- Track vocabulary that has been learned and words still to be studied.
- Review learned words using a five-level Leitner-style system, with review
  intervals of 1, 2, 5, 14 and 30 days.
- Store vocabulary and learning progress locally in JSON.

### Grammar

The application contains a morphological database of Greek words and their
inflected forms. Words are analysed for properties such as:

- part of speech
- case
- gender
- number
- tense
- voice
- person

A context-free grammar with feature information is used to parse Greek
sentences and construct parse trees.

### Sentence construction

Sentence exercises give the learner an English prompt and ask them to
construct the corresponding Greek sentence from their available vocabulary.

The application analyses the submitted sentence and checks:

- word forms and morphology
- grammatical roles
- agreement
- case
- articles
- verb properties
- translation against the expected sentence structure

It can also display the grammatical analysis of individual tokens and the
resulting parse tree.

### Accentuation

InflectedBlocks includes utilities for checking Ancient Greek sentential
accentuation. In particular, it handles the conversion of an acute accent to
a grave on the ultima of a non-final word in a clause.

## Implementation

The application is written in Python.

The main components are:

- `data.py` — Greek vocabulary, morphological data and sentence prompts
- `vocabulary.py` — vocabulary management and spaced review
- `grammar.py` — morphological analysis, grammar rules and chart parsing
- `sentences.py` — sentence construction and validation
- `accentuation.py` — Greek accentuation rules
- `ui.py` — terminal interface
- `main.py` — application loop and study modes

The terminal interface uses [Rich](https://github.com/Textualize/rich) for
formatted output, tables and interactive feedback.

## Running

Clone the repository and install the dependency:

```bash
git clone https://github.com/MartijnWallage/InflectedBlocks.git
cd InflectedBlocks
python -m pip install rich
```

Then run:

```bash
python main.py
```
