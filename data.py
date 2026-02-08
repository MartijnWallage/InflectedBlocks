"""Word database, sentence prompts, and inflection tables for Ancient Greek."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Word entries keyed by lemma
# ---------------------------------------------------------------------------

WORDS: dict[str, dict] = {
    # ── Articles ──────────────────────────────────────────────────────────
    "ὁ": {
        "lemma": "ὁ",
        "pos": "article",
        "meaning": "the",
        "forms": {
            # masculine
            "nom_sg_masc": "ὁ",
            "gen_sg_masc": "τοῦ",
            "dat_sg_masc": "τῷ",
            "acc_sg_masc": "τόν",
            "nom_pl_masc": "οἱ",
            "gen_pl_masc": "τῶν",
            "dat_pl_masc": "τοῖς",
            "acc_pl_masc": "τούς",
            # feminine
            "nom_sg_fem": "ἡ",
            "gen_sg_fem": "τῆς",
            "dat_sg_fem": "τῇ",
            "acc_sg_fem": "τήν",
            "nom_pl_fem": "αἱ",
            "gen_pl_fem": "τῶν",
            "dat_pl_fem": "ταῖς",
            "acc_pl_fem": "τάς",
            # neuter
            "nom_sg_neut": "τό",
            "gen_sg_neut": "τοῦ",
            "dat_sg_neut": "τῷ",
            "acc_sg_neut": "τό",
            "nom_pl_neut": "τά",
            "gen_pl_neut": "τῶν",
            "dat_pl_neut": "τοῖς",
            "acc_pl_neut": "τά",
        },
    },

    # ── Nouns ─────────────────────────────────────────────────────────────
    "ἄνθρωπος": {
        "lemma": "ἄνθρωπος",
        "pos": "noun",
        "meaning": "man, human being",
        "gender": "masculine",
        "declension": 2,
        "forms": {
            "nom_sg": "ἄνθρωπος", "gen_sg": "ἀνθρώπου",
            "dat_sg": "ἀνθρώπῳ",  "acc_sg": "ἄνθρωπον",
            "voc_sg": "ἄνθρωπε",
            "nom_pl": "ἄνθρωποι", "gen_pl": "ἀνθρώπων",
            "dat_pl": "ἀνθρώποις", "acc_pl": "ἀνθρώπους",
        },
    },
    "ἵππος": {
        "lemma": "ἵππος",
        "pos": "noun",
        "meaning": "horse",
        "gender": "masculine",
        "declension": 2,
        "forms": {
            "nom_sg": "ἵππος", "gen_sg": "ἵππου",
            "dat_sg": "ἵππῳ",  "acc_sg": "ἵππον",
            "voc_sg": "ἵππε",
            "nom_pl": "ἵπποι", "gen_pl": "ἵππων",
            "dat_pl": "ἵπποις", "acc_pl": "ἵππους",
        },
    },
    "λόγος": {
        "lemma": "λόγος",
        "pos": "noun",
        "meaning": "word, speech, reason",
        "gender": "masculine",
        "declension": 2,
        "forms": {
            "nom_sg": "λόγος", "gen_sg": "λόγου",
            "dat_sg": "λόγῳ",  "acc_sg": "λόγον",
            "voc_sg": "λόγε",
            "nom_pl": "λόγοι", "gen_pl": "λόγων",
            "dat_pl": "λόγοις", "acc_pl": "λόγους",
        },
    },
    "δῶρον": {
        "lemma": "δῶρον",
        "pos": "noun",
        "meaning": "gift",
        "gender": "neuter",
        "declension": 2,
        "forms": {
            "nom_sg": "δῶρον", "gen_sg": "δώρου",
            "dat_sg": "δώρῳ",  "acc_sg": "δῶρον",
            "voc_sg": "δῶρον",
            "nom_pl": "δῶρα",  "gen_pl": "δώρων",
            "dat_pl": "δώροις", "acc_pl": "δῶρα",
        },
    },
    "θεός": {
        "lemma": "θεός",
        "pos": "noun",
        "meaning": "god",
        "gender": "masculine",
        "declension": 2,
        "forms": {
            "nom_sg": "θεός", "gen_sg": "θεοῦ",
            "dat_sg": "θεῷ",  "acc_sg": "θεόν",
            "voc_sg": "θεέ",
            "nom_pl": "θεοί", "gen_pl": "θεῶν",
            "dat_pl": "θεοῖς", "acc_pl": "θεούς",
        },
    },
    "στρατιώτης": {
        "lemma": "στρατιώτης",
        "pos": "noun",
        "meaning": "soldier",
        "gender": "masculine",
        "declension": 1,
        "forms": {
            "nom_sg": "στρατιώτης", "gen_sg": "στρατιώτου",
            "dat_sg": "στρατιώτῃ",  "acc_sg": "στρατιώτην",
            "voc_sg": "στρατιῶτα",
            "nom_pl": "στρατιῶται", "gen_pl": "στρατιωτῶν",
            "dat_pl": "στρατιώταις", "acc_pl": "στρατιώτας",
        },
    },
    "ψυχή": {
        "lemma": "ψυχή",
        "pos": "noun",
        "meaning": "soul, spirit",
        "gender": "feminine",
        "declension": 1,
        "forms": {
            "nom_sg": "ψυχή",  "gen_sg": "ψυχῆς",
            "dat_sg": "ψυχῇ",  "acc_sg": "ψυχήν",
            "voc_sg": "ψυχή",
            "nom_pl": "ψυχαί", "gen_pl": "ψυχῶν",
            "dat_pl": "ψυχαῖς", "acc_pl": "ψυχάς",
        },
    },
    "θάλαττα": {
        "lemma": "θάλαττα",
        "pos": "noun",
        "meaning": "sea",
        "gender": "feminine",
        "declension": 1,
        "forms": {
            "nom_sg": "θάλαττα",  "gen_sg": "θαλάττης",
            "dat_sg": "θαλάττῃ",  "acc_sg": "θάλατταν",
            "voc_sg": "θάλαττα",
            "nom_pl": "θάλατται", "gen_pl": "θαλαττῶν",
            "dat_pl": "θαλάτταις", "acc_pl": "θαλάττας",
        },
    },
    "ἀλήθεια": {
        "lemma": "ἀλήθεια",
        "pos": "noun",
        "meaning": "truth",
        "gender": "feminine",
        "declension": 1,
        "forms": {
            "nom_sg": "ἀλήθεια",  "gen_sg": "ἀληθείας",
            "dat_sg": "ἀληθείᾳ",  "acc_sg": "ἀλήθειαν",
            "voc_sg": "ἀλήθεια",
            "nom_pl": "ἀλήθειαι", "gen_pl": "ἀληθειῶν",
            "dat_pl": "ἀληθείαις", "acc_pl": "ἀληθείας",
        },
    },
    "οἰκία": {
        "lemma": "οἰκία",
        "pos": "noun",
        "meaning": "house",
        "gender": "feminine",
        "declension": 1,
        "forms": {
            "nom_sg": "οἰκία",  "gen_sg": "οἰκίας",
            "dat_sg": "οἰκίᾳ",  "acc_sg": "οἰκίαν",
            "voc_sg": "οἰκία",
            "nom_pl": "οἰκίαι", "gen_pl": "οἰκιῶν",
            "dat_pl": "οἰκίαις", "acc_pl": "οἰκίας",
        },
    },
    "παιδίον": {
        "lemma": "παιδίον",
        "pos": "noun",
        "meaning": "child",
        "gender": "neuter",
        "declension": 2,
        "forms": {
            "nom_sg": "παιδίον", "gen_sg": "παιδίου",
            "dat_sg": "παιδίῳ",  "acc_sg": "παιδίον",
            "voc_sg": "παιδίον",
            "nom_pl": "παιδία",  "gen_pl": "παιδίων",
            "dat_pl": "παιδίοις", "acc_pl": "παιδία",
        },
    },
    "βιβλίον": {
        "lemma": "βιβλίον",
        "pos": "noun",
        "meaning": "book",
        "gender": "neuter",
        "declension": 2,
        "forms": {
            "nom_sg": "βιβλίον", "gen_sg": "βιβλίου",
            "dat_sg": "βιβλίῳ",  "acc_sg": "βιβλίον",
            "voc_sg": "βιβλίον",
            "nom_pl": "βιβλία",  "gen_pl": "βιβλίων",
            "dat_pl": "βιβλίοις", "acc_pl": "βιβλία",
        },
    },
    "πόλεμος": {
        "lemma": "πόλεμος",
        "pos": "noun",
        "meaning": "war",
        "gender": "masculine",
        "declension": 2,
        "forms": {
            "nom_sg": "πόλεμος", "gen_sg": "πολέμου",
            "dat_sg": "πολέμῳ",  "acc_sg": "πόλεμον",
            "voc_sg": "πόλεμε",
            "nom_pl": "πόλεμοι", "gen_pl": "πολέμων",
            "dat_pl": "πολέμοις", "acc_pl": "πολέμους",
        },
    },
    "εἰρήνη": {
        "lemma": "εἰρήνη",
        "pos": "noun",
        "meaning": "peace",
        "gender": "feminine",
        "declension": 1,
        "forms": {
            "nom_sg": "εἰρήνη",  "gen_sg": "εἰρήνης",
            "dat_sg": "εἰρήνῃ",  "acc_sg": "εἰρήνην",
            "voc_sg": "εἰρήνη",
            "nom_pl": "εἰρῆναι", "gen_pl": "εἰρηνῶν",
            "dat_pl": "εἰρήναις", "acc_pl": "εἰρήνας",
        },
    },
    "νῆσος": {
        "lemma": "νῆσος",
        "pos": "noun",
        "meaning": "island",
        "gender": "feminine",
        "declension": 2,
        "forms": {
            "nom_sg": "νῆσος", "gen_sg": "νήσου",
            "dat_sg": "νήσῳ",  "acc_sg": "νῆσον",
            "voc_sg": "νῆσε",
            "nom_pl": "νῆσοι", "gen_pl": "νήσων",
            "dat_pl": "νήσοις", "acc_pl": "νήσους",
        },
    },

    # ── Verbs ─────────────────────────────────────────────────────────────
    "λύω": {
        "lemma": "λύω",
        "pos": "verb",
        "meaning": "I loosen, release",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "λύω",
            "pres_act_ind_2sg": "λύεις",
            "pres_act_ind_3sg": "λύει",
            "pres_act_ind_1pl": "λύομεν",
            "pres_act_ind_2pl": "λύετε",
            "pres_act_ind_3pl": "λύουσι",
            "impf_act_ind_1sg": "ἔλυον",
            "impf_act_ind_2sg": "ἔλυες",
            "impf_act_ind_3sg": "ἔλυε",
            "impf_act_ind_1pl": "ἐλύομεν",
            "impf_act_ind_2pl": "ἐλύετε",
            "impf_act_ind_3pl": "ἔλυον",
            "fut_act_ind_1sg": "λύσω",
            "fut_act_ind_2sg": "λύσεις",
            "fut_act_ind_3sg": "λύσει",
            "fut_act_ind_1pl": "λύσομεν",
            "fut_act_ind_2pl": "λύσετε",
            "fut_act_ind_3pl": "λύσουσι",
            "aor_act_ind_1sg": "ἔλυσα",
            "aor_act_ind_2sg": "ἔλυσας",
            "aor_act_ind_3sg": "ἔλυσε",
            "aor_act_ind_1pl": "ἐλύσαμεν",
            "aor_act_ind_2pl": "ἐλύσατε",
            "aor_act_ind_3pl": "ἔλυσαν",
            "pres_act_inf": "λύειν",
        },
    },
    "γράφω": {
        "lemma": "γράφω",
        "pos": "verb",
        "meaning": "I write",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "γράφω",
            "pres_act_ind_2sg": "γράφεις",
            "pres_act_ind_3sg": "γράφει",
            "pres_act_ind_1pl": "γράφομεν",
            "pres_act_ind_2pl": "γράφετε",
            "pres_act_ind_3pl": "γράφουσι",
            "impf_act_ind_1sg": "ἔγραφον",
            "impf_act_ind_2sg": "ἔγραφες",
            "impf_act_ind_3sg": "ἔγραφε",
            "impf_act_ind_1pl": "ἐγράφομεν",
            "impf_act_ind_2pl": "ἐγράφετε",
            "impf_act_ind_3pl": "ἔγραφον",
            "fut_act_ind_1sg": "γράψω",
            "fut_act_ind_2sg": "γράψεις",
            "fut_act_ind_3sg": "γράψει",
            "fut_act_ind_1pl": "γράψομεν",
            "fut_act_ind_2pl": "γράψετε",
            "fut_act_ind_3pl": "γράψουσι",
            "aor_act_ind_1sg": "ἔγραψα",
            "aor_act_ind_2sg": "ἔγραψας",
            "aor_act_ind_3sg": "ἔγραψε",
            "aor_act_ind_1pl": "ἐγράψαμεν",
            "aor_act_ind_2pl": "ἐγράψατε",
            "aor_act_ind_3pl": "ἔγραψαν",
            "pres_act_inf": "γράφειν",
        },
    },
    "παιδεύω": {
        "lemma": "παιδεύω",
        "pos": "verb",
        "meaning": "I teach, educate",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "παιδεύω",
            "pres_act_ind_2sg": "παιδεύεις",
            "pres_act_ind_3sg": "παιδεύει",
            "pres_act_ind_1pl": "παιδεύομεν",
            "pres_act_ind_2pl": "παιδεύετε",
            "pres_act_ind_3pl": "παιδεύουσι",
            "impf_act_ind_1sg": "ἐπαίδευον",
            "impf_act_ind_2sg": "ἐπαίδευες",
            "impf_act_ind_3sg": "ἐπαίδευε",
            "impf_act_ind_1pl": "ἐπαιδεύομεν",
            "impf_act_ind_2pl": "ἐπαιδεύετε",
            "impf_act_ind_3pl": "ἐπαίδευον",
            "fut_act_ind_1sg": "παιδεύσω",
            "fut_act_ind_2sg": "παιδεύσεις",
            "fut_act_ind_3sg": "παιδεύσει",
            "fut_act_ind_1pl": "παιδεύσομεν",
            "fut_act_ind_2pl": "παιδεύσετε",
            "fut_act_ind_3pl": "παιδεύσουσι",
            "aor_act_ind_1sg": "ἐπαίδευσα",
            "aor_act_ind_2sg": "ἐπαίδευσας",
            "aor_act_ind_3sg": "ἐπαίδευσε",
            "aor_act_ind_1pl": "ἐπαιδεύσαμεν",
            "aor_act_ind_2pl": "ἐπαιδεύσατε",
            "aor_act_ind_3pl": "ἐπαίδευσαν",
            "pres_act_inf": "παιδεύειν",
        },
    },
    "πέμπω": {
        "lemma": "πέμπω",
        "pos": "verb",
        "meaning": "I send",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "πέμπω",
            "pres_act_ind_2sg": "πέμπεις",
            "pres_act_ind_3sg": "πέμπει",
            "pres_act_ind_1pl": "πέμπομεν",
            "pres_act_ind_2pl": "πέμπετε",
            "pres_act_ind_3pl": "πέμπουσι",
            "impf_act_ind_1sg": "ἔπεμπον",
            "impf_act_ind_2sg": "ἔπεμπες",
            "impf_act_ind_3sg": "ἔπεμπε",
            "impf_act_ind_1pl": "ἐπέμπομεν",
            "impf_act_ind_2pl": "ἐπέμπετε",
            "impf_act_ind_3pl": "ἔπεμπον",
            "fut_act_ind_1sg": "πέμψω",
            "fut_act_ind_2sg": "πέμψεις",
            "fut_act_ind_3sg": "πέμψει",
            "fut_act_ind_1pl": "πέμψομεν",
            "fut_act_ind_2pl": "πέμψετε",
            "fut_act_ind_3pl": "πέμψουσι",
            "aor_act_ind_1sg": "ἔπεμψα",
            "aor_act_ind_2sg": "ἔπεμψας",
            "aor_act_ind_3sg": "ἔπεμψε",
            "aor_act_ind_1pl": "ἐπέμψαμεν",
            "aor_act_ind_2pl": "ἐπέμψατε",
            "aor_act_ind_3pl": "ἔπεμψαν",
            "pres_act_inf": "πέμπειν",
        },
    },
    "φέρω": {
        "lemma": "φέρω",
        "pos": "verb",
        "meaning": "I carry, bear",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "φέρω",
            "pres_act_ind_2sg": "φέρεις",
            "pres_act_ind_3sg": "φέρει",
            "pres_act_ind_1pl": "φέρομεν",
            "pres_act_ind_2pl": "φέρετε",
            "pres_act_ind_3pl": "φέρουσι",
            "impf_act_ind_1sg": "ἔφερον",
            "impf_act_ind_2sg": "ἔφερες",
            "impf_act_ind_3sg": "ἔφερε",
            "impf_act_ind_1pl": "ἐφέρομεν",
            "impf_act_ind_2pl": "ἐφέρετε",
            "impf_act_ind_3pl": "ἔφερον",
            "fut_act_ind_1sg": "οἴσω",
            "fut_act_ind_2sg": "οἴσεις",
            "fut_act_ind_3sg": "οἴσει",
            "fut_act_ind_1pl": "οἴσομεν",
            "fut_act_ind_2pl": "οἴσετε",
            "fut_act_ind_3pl": "οἴσουσι",
            "aor_act_ind_1sg": "ἤνεγκα",
            "aor_act_ind_2sg": "ἤνεγκας",
            "aor_act_ind_3sg": "ἤνεγκε",
            "aor_act_ind_1pl": "ἠνέγκαμεν",
            "aor_act_ind_2pl": "ἠνέγκατε",
            "aor_act_ind_3pl": "ἤνεγκαν",
            "pres_act_inf": "φέρειν",
        },
    },
    "ἄγω": {
        "lemma": "ἄγω",
        "pos": "verb",
        "meaning": "I lead",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "ἄγω",
            "pres_act_ind_2sg": "ἄγεις",
            "pres_act_ind_3sg": "ἄγει",
            "pres_act_ind_1pl": "ἄγομεν",
            "pres_act_ind_2pl": "ἄγετε",
            "pres_act_ind_3pl": "ἄγουσι",
            "impf_act_ind_1sg": "ἦγον",
            "impf_act_ind_2sg": "ἦγες",
            "impf_act_ind_3sg": "ἦγε",
            "impf_act_ind_1pl": "ἤγομεν",
            "impf_act_ind_2pl": "ἤγετε",
            "impf_act_ind_3pl": "ἦγον",
            "fut_act_ind_1sg": "ἄξω",
            "fut_act_ind_2sg": "ἄξεις",
            "fut_act_ind_3sg": "ἄξει",
            "fut_act_ind_1pl": "ἄξομεν",
            "fut_act_ind_2pl": "ἄξετε",
            "fut_act_ind_3pl": "ἄξουσι",
            "aor_act_ind_1sg": "ἤγαγον",
            "aor_act_ind_2sg": "ἤγαγες",
            "aor_act_ind_3sg": "ἤγαγε",
            "aor_act_ind_1pl": "ἠγάγομεν",
            "aor_act_ind_2pl": "ἠγάγετε",
            "aor_act_ind_3pl": "ἤγαγον",
            "pres_act_inf": "ἄγειν",
        },
    },
    "λέγω": {
        "lemma": "λέγω",
        "pos": "verb",
        "meaning": "I say, speak",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "λέγω",
            "pres_act_ind_2sg": "λέγεις",
            "pres_act_ind_3sg": "λέγει",
            "pres_act_ind_1pl": "λέγομεν",
            "pres_act_ind_2pl": "λέγετε",
            "pres_act_ind_3pl": "λέγουσι",
            "impf_act_ind_1sg": "ἔλεγον",
            "impf_act_ind_2sg": "ἔλεγες",
            "impf_act_ind_3sg": "ἔλεγε",
            "impf_act_ind_1pl": "ἐλέγομεν",
            "impf_act_ind_2pl": "ἐλέγετε",
            "impf_act_ind_3pl": "ἔλεγον",
            "fut_act_ind_1sg": "λέξω",
            "fut_act_ind_2sg": "λέξεις",
            "fut_act_ind_3sg": "λέξει",
            "fut_act_ind_1pl": "λέξομεν",
            "fut_act_ind_2pl": "λέξετε",
            "fut_act_ind_3pl": "λέξουσι",
            "aor_act_ind_1sg": "ἔλεξα",
            "aor_act_ind_2sg": "ἔλεξας",
            "aor_act_ind_3sg": "ἔλεξε",
            "aor_act_ind_1pl": "ἐλέξαμεν",
            "aor_act_ind_2pl": "ἐλέξατε",
            "aor_act_ind_3pl": "ἔλεξαν",
            "pres_act_inf": "λέγειν",
        },
    },
    "ἔχω": {
        "lemma": "ἔχω",
        "pos": "verb",
        "meaning": "I have, hold",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "ἔχω",
            "pres_act_ind_2sg": "ἔχεις",
            "pres_act_ind_3sg": "ἔχει",
            "pres_act_ind_1pl": "ἔχομεν",
            "pres_act_ind_2pl": "ἔχετε",
            "pres_act_ind_3pl": "ἔχουσι",
            "impf_act_ind_1sg": "εἶχον",
            "impf_act_ind_2sg": "εἶχες",
            "impf_act_ind_3sg": "εἶχε",
            "impf_act_ind_1pl": "εἴχομεν",
            "impf_act_ind_2pl": "εἴχετε",
            "impf_act_ind_3pl": "εἶχον",
            "fut_act_ind_1sg": "ἕξω",
            "fut_act_ind_2sg": "ἕξεις",
            "fut_act_ind_3sg": "ἕξει",
            "fut_act_ind_1pl": "ἕξομεν",
            "fut_act_ind_2pl": "ἕξετε",
            "fut_act_ind_3pl": "ἕξουσι",
            "aor_act_ind_1sg": "ἔσχον",
            "aor_act_ind_2sg": "ἔσχες",
            "aor_act_ind_3sg": "ἔσχε",
            "aor_act_ind_1pl": "ἔσχομεν",
            "aor_act_ind_2pl": "ἔσχετε",
            "aor_act_ind_3pl": "ἔσχον",
            "pres_act_inf": "ἔχειν",
        },
    },
    "βλέπω": {
        "lemma": "βλέπω",
        "pos": "verb",
        "meaning": "I see, look",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "βλέπω",
            "pres_act_ind_2sg": "βλέπεις",
            "pres_act_ind_3sg": "βλέπει",
            "pres_act_ind_1pl": "βλέπομεν",
            "pres_act_ind_2pl": "βλέπετε",
            "pres_act_ind_3pl": "βλέπουσι",
            "impf_act_ind_1sg": "ἔβλεπον",
            "impf_act_ind_2sg": "ἔβλεπες",
            "impf_act_ind_3sg": "ἔβλεπε",
            "impf_act_ind_1pl": "ἐβλέπομεν",
            "impf_act_ind_2pl": "ἐβλέπετε",
            "impf_act_ind_3pl": "ἔβλεπον",
            "fut_act_ind_1sg": "βλέψω",
            "fut_act_ind_2sg": "βλέψεις",
            "fut_act_ind_3sg": "βλέψει",
            "fut_act_ind_1pl": "βλέψομεν",
            "fut_act_ind_2pl": "βλέψετε",
            "fut_act_ind_3pl": "βλέψουσι",
            "aor_act_ind_1sg": "ἔβλεψα",
            "aor_act_ind_2sg": "ἔβλεψας",
            "aor_act_ind_3sg": "ἔβλεψε",
            "aor_act_ind_1pl": "ἐβλέψαμεν",
            "aor_act_ind_2pl": "ἐβλέψατε",
            "aor_act_ind_3pl": "ἔβλεψαν",
            "pres_act_inf": "βλέπειν",
        },
    },
    "διδάσκω": {
        "lemma": "διδάσκω",
        "pos": "verb",
        "meaning": "I teach",
        "conjugation": "thematic",
        "forms": {
            "pres_act_ind_1sg": "διδάσκω",
            "pres_act_ind_2sg": "διδάσκεις",
            "pres_act_ind_3sg": "διδάσκει",
            "pres_act_ind_1pl": "διδάσκομεν",
            "pres_act_ind_2pl": "διδάσκετε",
            "pres_act_ind_3pl": "διδάσκουσι",
            "impf_act_ind_1sg": "ἐδίδασκον",
            "impf_act_ind_2sg": "ἐδίδασκες",
            "impf_act_ind_3sg": "ἐδίδασκε",
            "impf_act_ind_1pl": "ἐδιδάσκομεν",
            "impf_act_ind_2pl": "ἐδιδάσκετε",
            "impf_act_ind_3pl": "ἐδίδασκον",
            "fut_act_ind_1sg": "διδάξω",
            "fut_act_ind_2sg": "διδάξεις",
            "fut_act_ind_3sg": "διδάξει",
            "fut_act_ind_1pl": "διδάξομεν",
            "fut_act_ind_2pl": "διδάξετε",
            "fut_act_ind_3pl": "διδάξουσι",
            "aor_act_ind_1sg": "ἐδίδαξα",
            "aor_act_ind_2sg": "ἐδίδαξας",
            "aor_act_ind_3sg": "ἐδίδαξε",
            "aor_act_ind_1pl": "ἐδιδάξαμεν",
            "aor_act_ind_2pl": "ἐδιδάξατε",
            "aor_act_ind_3pl": "ἐδίδαξαν",
            "pres_act_inf": "διδάσκειν",
        },
    },

    # ── Adjectives ────────────────────────────────────────────────────────
    "ἀγαθός": {
        "lemma": "ἀγαθός",
        "pos": "adjective",
        "meaning": "good, noble",
        "forms": {
            # masculine
            "nom_sg_masc": "ἀγαθός", "gen_sg_masc": "ἀγαθοῦ",
            "dat_sg_masc": "ἀγαθῷ",  "acc_sg_masc": "ἀγαθόν",
            "nom_pl_masc": "ἀγαθοί", "gen_pl_masc": "ἀγαθῶν",
            "dat_pl_masc": "ἀγαθοῖς", "acc_pl_masc": "ἀγαθούς",
            # feminine
            "nom_sg_fem": "ἀγαθή",  "gen_sg_fem": "ἀγαθῆς",
            "dat_sg_fem": "ἀγαθῇ",  "acc_sg_fem": "ἀγαθήν",
            "nom_pl_fem": "ἀγαθαί", "gen_pl_fem": "ἀγαθῶν",
            "dat_pl_fem": "ἀγαθαῖς", "acc_pl_fem": "ἀγαθάς",
            # neuter
            "nom_sg_neut": "ἀγαθόν", "gen_sg_neut": "ἀγαθοῦ",
            "dat_sg_neut": "ἀγαθῷ",  "acc_sg_neut": "ἀγαθόν",
            "nom_pl_neut": "ἀγαθά",  "gen_pl_neut": "ἀγαθῶν",
            "dat_pl_neut": "ἀγαθοῖς", "acc_pl_neut": "ἀγαθά",
        },
    },
    "κακός": {
        "lemma": "κακός",
        "pos": "adjective",
        "meaning": "bad, evil",
        "forms": {
            "nom_sg_masc": "κακός", "gen_sg_masc": "κακοῦ",
            "dat_sg_masc": "κακῷ",  "acc_sg_masc": "κακόν",
            "nom_pl_masc": "κακοί", "gen_pl_masc": "κακῶν",
            "dat_pl_masc": "κακοῖς", "acc_pl_masc": "κακούς",
            "nom_sg_fem": "κακή",  "gen_sg_fem": "κακῆς",
            "dat_sg_fem": "κακῇ",  "acc_sg_fem": "κακήν",
            "nom_pl_fem": "κακαί", "gen_pl_fem": "κακῶν",
            "dat_pl_fem": "κακαῖς", "acc_pl_fem": "κακάς",
            "nom_sg_neut": "κακόν", "gen_sg_neut": "κακοῦ",
            "dat_sg_neut": "κακῷ",  "acc_sg_neut": "κακόν",
            "nom_pl_neut": "κακά",  "gen_pl_neut": "κακῶν",
            "dat_pl_neut": "κακοῖς", "acc_pl_neut": "κακά",
        },
    },
    "καλός": {
        "lemma": "καλός",
        "pos": "adjective",
        "meaning": "beautiful, fine",
        "forms": {
            "nom_sg_masc": "καλός", "gen_sg_masc": "καλοῦ",
            "dat_sg_masc": "καλῷ",  "acc_sg_masc": "καλόν",
            "nom_pl_masc": "καλοί", "gen_pl_masc": "καλῶν",
            "dat_pl_masc": "καλοῖς", "acc_pl_masc": "καλούς",
            "nom_sg_fem": "καλή",  "gen_sg_fem": "καλῆς",
            "dat_sg_fem": "καλῇ",  "acc_sg_fem": "καλήν",
            "nom_pl_fem": "καλαί", "gen_pl_fem": "καλῶν",
            "dat_pl_fem": "καλαῖς", "acc_pl_fem": "καλάς",
            "nom_sg_neut": "καλόν", "gen_sg_neut": "καλοῦ",
            "dat_sg_neut": "καλῷ",  "acc_sg_neut": "καλόν",
            "nom_pl_neut": "καλά",  "gen_pl_neut": "καλῶν",
            "dat_pl_neut": "καλοῖς", "acc_pl_neut": "καλά",
        },
    },
    "σοφός": {
        "lemma": "σοφός",
        "pos": "adjective",
        "meaning": "wise",
        "forms": {
            "nom_sg_masc": "σοφός", "gen_sg_masc": "σοφοῦ",
            "dat_sg_masc": "σοφῷ",  "acc_sg_masc": "σοφόν",
            "nom_pl_masc": "σοφοί", "gen_pl_masc": "σοφῶν",
            "dat_pl_masc": "σοφοῖς", "acc_pl_masc": "σοφούς",
            "nom_sg_fem": "σοφή",  "gen_sg_fem": "σοφῆς",
            "dat_sg_fem": "σοφῇ",  "acc_sg_fem": "σοφήν",
            "nom_pl_fem": "σοφαί", "gen_pl_fem": "σοφῶν",
            "dat_pl_fem": "σοφαῖς", "acc_pl_fem": "σοφάς",
            "nom_sg_neut": "σοφόν", "gen_sg_neut": "σοφοῦ",
            "dat_sg_neut": "σοφῷ",  "acc_sg_neut": "σοφόν",
            "nom_pl_neut": "σοφά",  "gen_pl_neut": "σοφῶν",
            "dat_pl_neut": "σοφοῖς", "acc_pl_neut": "σοφά",
        },
    },
    "μικρός": {
        "lemma": "μικρός",
        "pos": "adjective",
        "meaning": "small, little",
        "forms": {
            "nom_sg_masc": "μικρός", "gen_sg_masc": "μικροῦ",
            "dat_sg_masc": "μικρῷ",  "acc_sg_masc": "μικρόν",
            "nom_pl_masc": "μικροί", "gen_pl_masc": "μικρῶν",
            "dat_pl_masc": "μικροῖς", "acc_pl_masc": "μικρούς",
            "nom_sg_fem": "μικρά",  "gen_sg_fem": "μικρᾶς",
            "dat_sg_fem": "μικρᾷ",  "acc_sg_fem": "μικράν",
            "nom_pl_fem": "μικραί", "gen_pl_fem": "μικρῶν",
            "dat_pl_fem": "μικραῖς", "acc_pl_fem": "μικράς",
            "nom_sg_neut": "μικρόν", "gen_sg_neut": "μικροῦ",
            "dat_sg_neut": "μικρῷ",  "acc_sg_neut": "μικρόν",
            "nom_pl_neut": "μικρά",  "gen_pl_neut": "μικρῶν",
            "dat_pl_neut": "μικροῖς", "acc_pl_neut": "μικρά",
        },
    },
    "μέγας": {
        "lemma": "μέγας",
        "pos": "adjective",
        "meaning": "great, large",
        "forms": {
            "nom_sg_masc": "μέγας",  "gen_sg_masc": "μεγάλου",
            "dat_sg_masc": "μεγάλῳ", "acc_sg_masc": "μέγαν",
            "nom_pl_masc": "μεγάλοι", "gen_pl_masc": "μεγάλων",
            "dat_pl_masc": "μεγάλοις", "acc_pl_masc": "μεγάλους",
            "nom_sg_fem": "μεγάλη",  "gen_sg_fem": "μεγάλης",
            "dat_sg_fem": "μεγάλῃ",  "acc_sg_fem": "μεγάλην",
            "nom_pl_fem": "μεγάλαι", "gen_pl_fem": "μεγάλων",
            "dat_pl_fem": "μεγάλαις", "acc_pl_fem": "μεγάλας",
            "nom_sg_neut": "μέγα",   "gen_sg_neut": "μεγάλου",
            "dat_sg_neut": "μεγάλῳ", "acc_sg_neut": "μέγα",
            "nom_pl_neut": "μεγάλα", "gen_pl_neut": "μεγάλων",
            "dat_pl_neut": "μεγάλοις", "acc_pl_neut": "μεγάλα",
        },
    },
    "δίκαιος": {
        "lemma": "δίκαιος",
        "pos": "adjective",
        "meaning": "just, righteous",
        "forms": {
            "nom_sg_masc": "δίκαιος", "gen_sg_masc": "δικαίου",
            "dat_sg_masc": "δικαίῳ",  "acc_sg_masc": "δίκαιον",
            "nom_pl_masc": "δίκαιοι", "gen_pl_masc": "δικαίων",
            "dat_pl_masc": "δικαίοις", "acc_pl_masc": "δικαίους",
            "nom_sg_fem": "δικαία",  "gen_sg_fem": "δικαίας",
            "dat_sg_fem": "δικαίᾳ",  "acc_sg_fem": "δικαίαν",
            "nom_pl_fem": "δίκαιαι", "gen_pl_fem": "δικαίων",
            "dat_pl_fem": "δικαίαις", "acc_pl_fem": "δικαίας",
            "nom_sg_neut": "δίκαιον", "gen_sg_neut": "δικαίου",
            "dat_sg_neut": "δικαίῳ",  "acc_sg_neut": "δίκαιον",
            "nom_pl_neut": "δίκαια",  "gen_pl_neut": "δικαίων",
            "dat_pl_neut": "δικαίοις", "acc_pl_neut": "δίκαια",
        },
    },
    "ἄξιος": {
        "lemma": "ἄξιος",
        "pos": "adjective",
        "meaning": "worthy, deserving",
        "forms": {
            "nom_sg_masc": "ἄξιος", "gen_sg_masc": "ἀξίου",
            "dat_sg_masc": "ἀξίῳ",  "acc_sg_masc": "ἄξιον",
            "nom_pl_masc": "ἄξιοι", "gen_pl_masc": "ἀξίων",
            "dat_pl_masc": "ἀξίοις", "acc_pl_masc": "ἀξίους",
            "nom_sg_fem": "ἀξία",  "gen_sg_fem": "ἀξίας",
            "dat_sg_fem": "ἀξίᾳ",  "acc_sg_fem": "ἀξίαν",
            "nom_pl_fem": "ἄξιαι", "gen_pl_fem": "ἀξίων",
            "dat_pl_fem": "ἀξίαις", "acc_pl_fem": "ἀξίας",
            "nom_sg_neut": "ἄξιον", "gen_sg_neut": "ἀξίου",
            "dat_sg_neut": "ἀξίῳ",  "acc_sg_neut": "ἄξιον",
            "nom_pl_neut": "ἄξια",  "gen_pl_neut": "ἀξίων",
            "dat_pl_neut": "ἀξίοις", "acc_pl_neut": "ἄξια",
        },
    },

    # ── Prepositions ──────────────────────────────────────────────────────
    "ἐν": {
        "lemma": "ἐν",
        "pos": "preposition",
        "meaning": "in (+ dative)",
        "governs": "dat",
        "forms": {"base": "ἐν"},
    },
    "εἰς": {
        "lemma": "εἰς",
        "pos": "preposition",
        "meaning": "into, to (+ accusative)",
        "governs": "acc",
        "forms": {"base": "εἰς"},
    },
    "ἐκ": {
        "lemma": "ἐκ",
        "pos": "preposition",
        "meaning": "out of, from (+ genitive)",
        "governs": "gen",
        "forms": {"base": "ἐκ"},
    },
    "πρός": {
        "lemma": "πρός",
        "pos": "preposition",
        "meaning": "to, toward (+ accusative)",
        "governs": "acc",
        "forms": {"base": "πρός"},
    },
    "ἀπό": {
        "lemma": "ἀπό",
        "pos": "preposition",
        "meaning": "from, away from (+ genitive)",
        "governs": "gen",
        "forms": {"base": "ἀπό"},
    },

    # ── Conjunctions ──────────────────────────────────────────────────────
    "καί": {
        "lemma": "καί",
        "pos": "conjunction",
        "meaning": "and",
        "forms": {"base": "καί"},
    },
    "ἀλλά": {
        "lemma": "ἀλλά",
        "pos": "conjunction",
        "meaning": "but",
        "forms": {"base": "ἀλλά"},
    },
}


# ---------------------------------------------------------------------------
# Reverse index: inflected form → list of (lemma, pos, features)
# ---------------------------------------------------------------------------

_FORM_INDEX: dict[str, list[tuple[str, str, dict]]] | None = None


GENDER_NORMALIZE = {
    "masculine": "masc", "feminine": "fem", "neuter": "neut",
    "masc": "masc", "fem": "fem", "neut": "neut",
}


def _parse_noun_key(key: str, entry: dict) -> dict:
    """Parse a noun form key like 'nom_sg' into feature dict."""
    parts = key.split("_")
    if len(parts) == 2:
        case, number = parts
        gender = GENDER_NORMALIZE.get(entry["gender"], entry["gender"])
        return {
            "case": case, "number": number, "gender": gender,
        }
    return {}


def _parse_article_or_adj_key(key: str) -> dict:
    """Parse a key like 'nom_sg_masc' into feature dict."""
    parts = key.split("_")
    if len(parts) == 3:
        case, number, gender = parts
        return {"case": case, "number": number, "gender": gender}
    return {}


def _parse_verb_key(key: str) -> dict:
    """Parse a verb form key like 'pres_act_ind_3sg' into feature dict."""
    parts = key.split("_")
    if len(parts) == 4:
        tense, voice, mood, pn = parts
        person = pn[0]
        number = pn[1:]
        return {
            "tense": tense, "voice": voice, "mood": mood,
            "person": person, "number": number,
        }
    if len(parts) == 3 and parts[2] == "inf":
        return {"tense": parts[0], "voice": parts[1], "mood": "inf"}
    return {}


def _build_form_index() -> dict[str, list[tuple[str, str, dict]]]:
    """Build a reverse index from surface form → (lemma, pos, features)."""
    index: dict[str, list[tuple[str, str, dict]]] = {}
    for lemma, entry in WORDS.items():
        pos = entry["pos"]
        for key, form in entry["forms"].items():
            # Handle ν-movable forms like "λύουσι(ν)"
            forms_to_add = [form]
            if "(ν)" in form:
                base = form.replace("(ν)", "")
                forms_to_add = [base, base + "ν"]

            if pos == "noun":
                features = _parse_noun_key(key, entry)
            elif pos in ("article", "adjective"):
                features = _parse_article_or_adj_key(key)
            elif pos == "verb":
                features = _parse_verb_key(key)
            elif pos == "preposition":
                features = {"governs": entry.get("governs", "")}
            elif pos == "conjunction":
                features = {}
            else:
                features = {}

            for f in forms_to_add:
                if f not in index:
                    index[f] = []
                index[f].append((lemma, pos, features))
    return index


def get_form_index() -> dict[str, list[tuple[str, str, dict]]]:
    """Return the (lazily built) form index."""
    global _FORM_INDEX
    if _FORM_INDEX is None:
        _FORM_INDEX = _build_form_index()
    return _FORM_INDEX


def lookup_form(form_string: str) -> list[tuple[str, str, dict]]:
    """Look up an inflected form and return all possible analyses.

    Normalizes graves to acutes before lookup so that sentential forms
    (e.g. ἀγαθὸν with grave) still match citation forms (ἀγαθόν with acute).

    Returns list of (lemma, pos, features) tuples.
    """
    from accentuation import normalize_graves
    idx = get_form_index()
    normalized = normalize_graves(form_string)
    return idx.get(normalized, [])


# ---------------------------------------------------------------------------
# Sentence prompts
# ---------------------------------------------------------------------------

PROMPTS: list[dict] = [
    {
        "english": "The man releases the horse.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λύω", "ἵππος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λύω",
            "tense": "pres",
            "object": {"noun": "ἵππος"},
        },
    },
    {
        "english": "The soldier writes a book.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc, no article)",
        "required_lemmas": ["ὁ", "στρατιώτης", "γράφω", "βιβλίον"],
        "expected": {
            "subject": {"noun": "στρατιώτης"},
            "verb": "γράφω",
            "tense": "pres",
            "object": {"noun": "βιβλίον", "indef": True},
        },
    },
    {
        "english": "The good man teaches the child.",
        "hint": "Article + adjective + noun (nom) + verb (3sg pres act) + article + noun (acc)",
        "required_lemmas": ["ὁ", "ἀγαθός", "ἄνθρωπος", "παιδεύω", "παιδίον"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος", "adj": "ἀγαθός"},
            "verb": "παιδεύω",
            "tense": "pres",
            "object": {"noun": "παιδίον"},
        },
    },
    {
        "english": "The god sends a gift.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc, no article)",
        "required_lemmas": ["ὁ", "θεός", "πέμπω", "δῶρον"],
        "expected": {
            "subject": {"noun": "θεός"},
            "verb": "πέμπω",
            "tense": "pres",
            "object": {"noun": "δῶρον", "indef": True},
        },
    },
    {
        "english": "The wise man has the truth.",
        "hint": "Article + adjective + noun (nom) + verb (3sg pres act) + article + noun (acc)",
        "required_lemmas": ["ὁ", "σοφός", "ἄνθρωπος", "ἔχω", "ἀλήθεια"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος", "adj": "σοφός"},
            "verb": "ἔχω",
            "tense": "pres",
            "object": {"noun": "ἀλήθεια"},
        },
    },
    {
        "english": "The man sees the sea.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "βλέπω", "θάλαττα"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "βλέπω",
            "tense": "pres",
            "object": {"noun": "θάλαττα"},
        },
    },
    {
        "english": "The soldier leads the horse into the house.",
        "hint": "Subject + verb (3sg pres act) + object + preposition (εἰς + acc) + noun",
        "required_lemmas": ["ὁ", "στρατιώτης", "ἄγω", "ἵππος", "εἰς", "οἰκία"],
        "expected": {
            "subject": {"noun": "στρατιώτης"},
            "verb": "ἄγω",
            "tense": "pres",
            "object": {"noun": "ἵππος"},
            "pp": {"prep": "εἰς", "noun": "οἰκία"},
        },
    },
    {
        "english": "The man carries the book out of the house.",
        "hint": "Subject + verb (3sg pres act) + object + preposition (ἐκ + gen) + noun",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "φέρω", "βιβλίον", "ἐκ", "οἰκία"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "φέρω",
            "tense": "pres",
            "object": {"noun": "βιβλίον"},
            "pp": {"prep": "ἐκ", "noun": "οἰκία"},
        },
    },
    {
        "english": "The man says the word.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λέγω", "λόγος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λέγω",
            "tense": "pres",
            "object": {"noun": "λόγος"},
        },
    },
    {
        "english": "The just man sees the beautiful gift.",
        "hint": "Article + adjective + noun (nom) + verb (3sg pres act) + article + adjective + noun (acc)",
        "required_lemmas": ["ὁ", "δίκαιος", "ἄνθρωπος", "βλέπω", "καλός", "δῶρον"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος", "adj": "δίκαιος"},
            "verb": "βλέπω",
            "tense": "pres",
            "object": {"noun": "δῶρον", "adj": "καλός"},
        },
    },
    # ── Imperfect tense prompts ──────────────────────────────────────────
    {
        "english": "The man was releasing the horse.",
        "hint": "Subject (nom) + verb (3sg impf act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λύω", "ἵππος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λύω",
            "tense": "impf",
            "object": {"noun": "ἵππος"},
        },
    },
    {
        "english": "The soldier was writing a book.",
        "hint": "Subject (nom) + verb (3sg impf act) + object (acc, no article)",
        "required_lemmas": ["ὁ", "στρατιώτης", "γράφω", "βιβλίον"],
        "expected": {
            "subject": {"noun": "στρατιώτης"},
            "verb": "γράφω",
            "tense": "impf",
            "object": {"noun": "βιβλίον", "indef": True},
        },
    },
    {
        "english": "The man was carrying the gift.",
        "hint": "Subject (nom) + verb (3sg impf act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "φέρω", "δῶρον"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "φέρω",
            "tense": "impf",
            "object": {"noun": "δῶρον"},
        },
    },
    # ── Future tense prompts ─────────────────────────────────────────────
    {
        "english": "The man will release the horse.",
        "hint": "Subject (nom) + verb (3sg fut act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λύω", "ἵππος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λύω",
            "tense": "fut",
            "object": {"noun": "ἵππος"},
        },
    },
    {
        "english": "The god will send a gift.",
        "hint": "Subject (nom) + verb (3sg fut act) + object (acc, no article)",
        "required_lemmas": ["ὁ", "θεός", "πέμπω", "δῶρον"],
        "expected": {
            "subject": {"noun": "θεός"},
            "verb": "πέμπω",
            "tense": "fut",
            "object": {"noun": "δῶρον", "indef": True},
        },
    },
    {
        "english": "The soldier will lead the horse into the house.",
        "hint": "Subject + verb (3sg fut act) + object + preposition (εἰς + acc) + noun",
        "required_lemmas": ["ὁ", "στρατιώτης", "ἄγω", "ἵππος", "εἰς", "οἰκία"],
        "expected": {
            "subject": {"noun": "στρατιώτης"},
            "verb": "ἄγω",
            "tense": "fut",
            "object": {"noun": "ἵππος"},
            "pp": {"prep": "εἰς", "noun": "οἰκία"},
        },
    },
    # ── Aorist tense prompts ─────────────────────────────────────────────
    {
        "english": "The man released the horse.",
        "hint": "Subject (nom) + verb (3sg aor act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λύω", "ἵππος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λύω",
            "tense": "aor",
            "object": {"noun": "ἵππος"},
        },
    },
    {
        "english": "The soldier wrote a book.",
        "hint": "Subject (nom) + verb (3sg aor act) + object (acc, no article)",
        "required_lemmas": ["ὁ", "στρατιώτης", "γράφω", "βιβλίον"],
        "expected": {
            "subject": {"noun": "στρατιώτης"},
            "verb": "γράφω",
            "tense": "aor",
            "object": {"noun": "βιβλίον", "indef": True},
        },
    },
    {
        "english": "The man said the word.",
        "hint": "Subject (nom) + verb (3sg aor act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λέγω", "λόγος"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "λέγω",
            "tense": "aor",
            "object": {"noun": "λόγος"},
        },
    },
    {
        "english": "The man carried the book out of the house.",
        "hint": "Subject + verb (3sg aor act) + object + preposition (ἐκ + gen) + noun",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "φέρω", "βιβλίον", "ἐκ", "οἰκία"],
        "expected": {
            "subject": {"noun": "ἄνθρωπος"},
            "verb": "φέρω",
            "tense": "aor",
            "object": {"noun": "βιβλίον"},
            "pp": {"prep": "ἐκ", "noun": "οἰκία"},
        },
    },
]
