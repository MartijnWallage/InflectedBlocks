// Flashcard model class
export class Flashcard {
    constructor(type, greekWord, englishTranslation, inflections = {}) {
        this.type = type;
        this.greekWord = greekWord;
        this.englishTranslation = englishTranslation;
        this.inflections = inflections;
        this.id = Date.now().toString();
    }

    static fromJSON(json) {
        return new Flashcard(json.type, json.greekWord, json.englishTranslation, json.inflections);
    }

    toJSON() {
        return {
            id: this.id,
            type: this.type,
            greekWord: this.greekWord,
            englishTranslation: this.englishTranslation,
            inflections: this.inflections
        };
    }
}
