export class PrologService {
    constructor() {
        this.session = null;
    }

    async initialize(databasePath = 'grammar.pl') {
        try {
            this.session = pl.create();
            const response = await fetch(databasePath);
            const program = await response.text();
            await this.session.consult(program);
            return true;
        } catch (e) {
            console.error('Error initializing Prolog:', e);
            return false;
        }
    }

    async assertWord(word, type) {
        if (!this.session) return false;
        
        try {
            const query = `retractall(word_type(${word}, _)), assertz(word_type(${word}, ${type})).`;
            return new Promise((resolve) => {
                this.session.query(query, {
                    success: () => {
                        this.session.answer({
                            success: () => resolve(true),
                            fail: () => resolve(false),
                            error: () => resolve(false)
                        });
                    },
                    error: () => resolve(false)
                });
            });
        } catch (e) {
            console.error('Error asserting word:', e);
            return false;
        }
    }

    async isValidSentence(words) {
        if (!this.session) return false;

        try {
            const wordList = words.map(w => `'${w}'`).join(',');
            const query = `valid_sentence([${wordList}]).`;
            
            return new Promise((resolve) => {
                this.session.query(query, {
                    success: () => {
                        this.session.answer({
                            success: () => resolve(true),
                            fail: () => resolve(false),
                            error: () => resolve(false)
                        });
                    },
                    error: () => resolve(false)
                });
            });
        } catch (e) {
            console.error('Error validating sentence:', e);
            return false;
        }
    }
}
