:- dynamic(word_type/2).
:- dynamic(word_translation/2).
:- dynamic(word_inflection/3).

member(X,[X|_]).
member(X,[_|Xs]) :- member(X,Xs).

word_type('kai',conjunction).
word_type('lego',verb).
word_translation('kai','and').
word_translation('lego','I speak').
word_inflection('lego',present3p,'legousin').
word_inflection('lego',present2p,'legete').
word_inflection('lego',present1p,'legomen').
word_inflection('lego',present3s,'legei').
word_inflection('lego',present2s,'legeis').
word_inflection('lego',present1s,'lego').

valid_sentence(Words) :- member(Word,Words), word_type(Word,verb).
