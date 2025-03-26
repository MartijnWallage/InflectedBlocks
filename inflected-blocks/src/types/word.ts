export enum WordType {
  Verb = 'verb',
  Noun = 'noun',
  Adjective = 'adjective',
  Adverb = 'adverb',
  Conjunction = 'conjunction',
  Preposition = 'preposition',
  Pronoun = 'pronoun',
  Article = 'article',
  Other = 'other'
}

export interface Inflection {
  form: string;
  description: string;
}

export interface Word {
  lemma: string;
  translation: string;
  wordType: WordType;
  inflections: Inflection[];
} 