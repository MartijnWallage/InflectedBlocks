member(X,[X|_]).
member(X,[_|Xs]) :- member(X,Xs).

:- dynamic(word_type/2).

word_type(runs, verb).
word_type(rabbit, noun).

valid_sentence(Words) :-
    word_type(Word, verb),
    member(Word, Words).