% Sentence structure rules
sentence(Sentence) :-
    valid_sentence(Sentence).

% Valid sentence:
% A sentence is valid if it has more than one word
valid_sentence([_, _|_]).

% Invalid sentence:
% A sentence is invalid if it has only one word
valid_sentence([_]) :- fail.