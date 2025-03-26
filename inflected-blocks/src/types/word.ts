export interface Inflection {
  form: string;
  description: string;
}

export interface Word {
  lemma: string;
  translation: string;
  inflections: Inflection[];
} 