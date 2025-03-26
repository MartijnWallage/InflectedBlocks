import { Word } from '../types/word';

const STORAGE_KEY = 'inflected-blocks-words';

export const saveWord = (word: Word): void => {
  const existingWords = getWords();
  existingWords.push(word);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(existingWords));
};

export const getWords = (): Word[] => {
  const storedWords = localStorage.getItem(STORAGE_KEY);
  return storedWords ? JSON.parse(storedWords) : [];
};

export const deleteWord = (index: number): void => {
  const words = getWords();
  words.splice(index, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(words));
}; 