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
            "acc_sg_masc": "τὸν",
            "nom_pl_masc": "οἱ",
            "gen_pl_masc": "τῶν",
            "dat_pl_masc": "τοῖς",
            "acc_pl_masc": "τοὺς",
            # feminine
            "nom_sg_fem": "ἡ",
            "gen_sg_fem": "τῆς",
            "dat_sg_fem": "τῇ",
            "acc_sg_fem": "τὴν",
            "nom_pl_fem": "αἱ",
            "gen_pl_fem": "τῶν",
            "dat_pl_fem": "ταῖς",
            "acc_pl_fem": "τὰς",
            # neuter
            "nom_sg_neut": "τὸ",
            "gen_sg_neut": "τοῦ",
            "dat_sg_neut": "τῷ",
            "acc_sg_neut": "τὸ",
            "nom_pl_neut": "τὰ",
            "gen_pl_neut": "τῶν",
            "dat_pl_neut": "τοῖς",
            "acc_pl_neut": "τὰ",
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

    Returns list of (lemma, pos, features) tuples.
    """
    idx = get_form_index()
    return idx.get(form_string, [])


# ---------------------------------------------------------------------------
# Sentence prompts
# ---------------------------------------------------------------------------

PROMPTS: list[dict] = [
    {
        "english": "The man releases the horse.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λύω", "ἵππος"],
    },
    {
        "english": "The soldier writes a book.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "στρατιώτης", "γράφω", "βιβλίον"],
    },
    {
        "english": "The good man teaches the child.",
        "hint": "Article + adjective + noun (nom) + verb (3sg) + article + noun (acc)",
        "required_lemmas": ["ὁ", "ἀγαθός", "ἄνθρωπος", "παιδεύω", "παιδίον"],
    },
    {
        "english": "The god sends a gift.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "θεός", "πέμπω", "δῶρον"],
    },
    {
        "english": "The wise man has the truth.",
        "hint": "Article + adjective + noun (nom) + verb (3sg) + article + noun (acc)",
        "required_lemmas": ["ὁ", "σοφός", "ἄνθρωπος", "ἔχω", "ἀλήθεια"],
    },
    {
        "english": "The man sees the sea.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "βλέπω", "θάλαττα"],
    },
    {
        "english": "The soldier leads the horse into the house.",
        "hint": "Subject + verb + object + preposition (εἰς + acc) + noun",
        "required_lemmas": ["ὁ", "στρατιώτης", "ἄγω", "ἵππος", "εἰς", "οἰκία"],
    },
    {
        "english": "The man carries the book out of the house.",
        "hint": "Subject + verb + object + preposition (ἐκ + gen) + noun",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "φέρω", "βιβλίον", "ἐκ", "οἰκία"],
    },
    {
        "english": "The man says the word.",
        "hint": "Subject (nom) + verb (3sg pres act) + object (acc)",
        "required_lemmas": ["ὁ", "ἄνθρωπος", "λέγω", "λόγος"],
    },
    {
        "english": "The just man sees the beautiful gift.",
        "hint": "Article + adjective + noun (nom) + verb (3sg) + article + adjective + noun (acc)",
        "required_lemmas": ["ὁ", "δίκαιος", "ἄνθρωπος", "βλέπω", "καλός", "δῶρον"],
    },
]
