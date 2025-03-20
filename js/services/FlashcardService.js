import { Flashcard } from '../models/Flashcard.js';

export class FlashcardService {
    constructor(storageKey = 'ancient_greek_flashcards') {
        this.storageKey = storageKey;
        this.flashcards = this.loadFromStorage();
    }

    loadFromStorage() {
        const stored = localStorage.getItem(this.storageKey);
        if (!stored) return [];
        try {
            const data = JSON.parse(stored);
            return data.map(item => Flashcard.fromJSON(item));
        } catch (e) {
            console.error('Error loading flashcards:', e);
            return [];
        }
    }

    saveToStorage() {
        try {
            const data = this.flashcards.map(card => card.toJSON());
            localStorage.setItem(this.storageKey, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('Error saving flashcards:', e);
            return false;
        }
    }

    addFlashcard(flashcard) {
        this.flashcards.push(flashcard);
        this.saveToStorage();
    }

    removeFlashcard(id) {
        this.flashcards = this.flashcards.filter(card => card.id !== id);
        this.saveToStorage();
    }

    getFlashcards() {
        return this.flashcards;
    }

    findByType(type) {
        return this.flashcards.filter(card => card.type === type);
    }

    findByWord(word) {
        return this.flashcards.find(card => card.greekWord === word);
    }
}
