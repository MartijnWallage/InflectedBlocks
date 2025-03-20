:- dynamic(word_type/2).
:- dynamic(word_translation/2).
:- dynamic(word_inflection/3).

member(X,[X|_]).
member(X,[_|Xs]) :- member(X,Xs).

% Verbs
word_type('λεγω',verb).
word_type('γιγνωσκω',verb).
word_type('ειμι',verb).

word_translation('λεγω','I speak').
word_translation('γιγνωσκω','I know').
word_translation('ειμι','I am').

word_inflection('λεγω',present3p,'λεγουσιν').
word_inflection('λεγω',present2p,'λεγετε').
word_inflection('λεγω',present1p,'λεγομεν').
word_inflection('λεγω',present3s,'λεγει').
word_inflection('λεγω',present2s,'λεγεις').
word_inflection('λεγω',present1s,'λεγω').

word_inflection('γιγνωσκω',present3p,'γιγνωσκουσιν').
word_inflection('γιγνωσκω',present2p,'γιγνωσκετε').
word_inflection('γιγνωσκω',present1p,'γιγνωσκομεν').
word_inflection('γιγνωσκω',present3s,'γιγνωσκει').
word_inflection('γιγνωσκω',present2s,'γιγνωσκεις').
word_inflection('γιγνωσκω',present1s,'γιγνωσκω').

word_inflection('ειμι',present3p,'εισιν').
word_inflection('ειμι',present2p,'εστε').
word_inflection('ειμι',present1p,'εσμεν').
word_inflection('ειμι',present3s,'εστιν').
word_inflection('ειμι',present2s,'ει').
word_inflection('ειμι',present1s,'ειμι').

% Nouns
word_type('ανθρωπος',noun).
word_type('πολις',noun).
word_type('θεος',noun).

word_translation('ανθρωπος','human being').
word_translation('πολις','city').
word_translation('θεος','god').

word_inflection('ανθρωπος',nomS,'ανθρωπος').
word_inflection('ανθρωπος',genS,'ανθρωπου').
word_inflection('ανθρωπος',datS,'ανθρωπω').
word_inflection('ανθρωπος',accS,'ανθρωπον').
word_inflection('ανθρωπος',vocS,'ανθρωπε').
word_inflection('ανθρωπος',nomP,'ανθρωποι').
word_inflection('ανθρωπος',genP,'ανθρωπων').
word_inflection('ανθρωπος',datP,'ανθρωποις').
word_inflection('ανθρωπος',accP,'ανθρωπους').
word_inflection('ανθρωπος',vocP,'ανθρωποι').

word_inflection('πολις',nomS,'πολις').
word_inflection('πολις',genS,'πολεως').
word_inflection('πολις',datS,'πολει').
word_inflection('πολις',accS,'πολιν').
word_inflection('πολις',vocS,'πολι').
word_inflection('πολις',nomP,'πολεις').
word_inflection('πολις',genP,'πολεων').
word_inflection('πολις',datP,'πολεσι').
word_inflection('πολις',accP,'πολεις').
word_inflection('πολις',vocP,'πολεις').

word_inflection('θεος',nomS,'θεος').
word_inflection('θεος',genS,'θεου').
word_inflection('θεος',datS,'θεω').
word_inflection('θεος',accS,'θεον').
word_inflection('θεος',vocS,'θεε').
word_inflection('θεος',nomP,'θεοι').
word_inflection('θεος',genP,'θεων').
word_inflection('θεος',datP,'θεοις').
word_inflection('θεος',accP,'θεους').
word_inflection('θεος',vocP,'θεοι').

% Adjectives
word_type('καλος',adjective).
word_type('σοφος',adjective).
word_type('μεγας',adjective).

word_translation('καλος','beautiful').
word_translation('σοφος','wise').
word_translation('μεγας','great').

word_inflection('καλος',mNomS,'καλος').
word_inflection('καλος',fNomS,'καλη').
word_inflection('καλος',nNomS,'καλον').
word_inflection('καλος',mAccS,'καλον').
word_inflection('καλος',fAccS,'καλην').
word_inflection('καλος',nAccS,'καλον').

word_inflection('σοφος',mNomS,'σοφος').
word_inflection('σοφος',fNomS,'σοφη').
word_inflection('σοφος',nNomS,'σοφον').
word_inflection('σοφος',mAccS,'σοφον').
word_inflection('σοφος',fAccS,'σοφην').
word_inflection('σοφος',nAccS,'σοφον').

word_inflection('μεγας',mNomS,'μεγας').
word_inflection('μεγας',fNomS,'μεγαλη').
word_inflection('μεγας',nNomS,'μεγα').
word_inflection('μεγας',mAccS,'μεγαν').
word_inflection('μεγας',fAccS,'μεγαλην').
word_inflection('μεγας',nAccS,'μεγα').

% Adverbs
word_type('καλως',adverb).
word_type('σοφως',adverb).
word_type('μεγαλως',adverb).

word_translation('καλως','beautifully').
word_translation('σοφως','wisely').
word_translation('μεγαλως','greatly').

% Prepositions
word_type('εν',preposition).
word_type('εις',preposition).
word_type('εκ',preposition).

word_translation('εν','in').
word_translation('εις','into').
word_translation('εκ','out of').

% Conjunctions
word_type('και',conjunction).
word_type('αλλ',conjunction).
word_type('γαρ',conjunction).

word_translation('και','and').
word_translation('αλλ','but').
word_translation('γαρ','for').

valid_sentence(Words) :- member(Word,Words), word_type(Word,verb).
