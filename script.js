// Store flashcards in memory (later we can add persistence)
let flashcards = [];
let currentCardIndex = 0;

// Storage key for localStorage
const STORAGE_KEY = 'ancient_greek_flashcards';

// DOM Elements
let flashcardContainer;
let addFlashcardBtn;
let flashcardForm;
let newFlashcardForm;
let cancelFlashcardBtn;
let wordTypeSelect;
let inflectionFields;
let toggleFlashcardsBtn;
let prevCardBtn;
let nextCardBtn;
let cardCounter;
let wordInput;
let wordSuggestions;
let sentenceDisplay;
let sentenceBlocks;
let currentBlock;
let blockInput;
let blockSuggestions;
let flashcardSuggestion;
let addNewFlashcardBtn;

// Word type configurations
const wordTypeConfigs = {
    verb: {
        label: 'Verb',
        inflections: [
            { label: 'Present Indicative Active 1st Person Singular', key: 'present1s' },
            { label: 'Present Indicative Active 2nd Person Singular', key: 'present2s' },
            { label: 'Present Indicative Active 3rd Person Singular', key: 'present3s' },
            { label: 'Present Indicative Active 1st Person Plural', key: 'present1p' },
            { label: 'Present Indicative Active 2nd Person Plural', key: 'present2p' },
            { label: 'Present Indicative Active 3rd Person Plural', key: 'present3p' }
        ]
    },
    noun: {
        label: 'Noun',
        inflections: [
            { label: 'Nominative Singular', key: 'nomS' },
            { label: 'Genitive Singular', key: 'genS' },
            { label: 'Dative Singular', key: 'datS' },
            { label: 'Accusative Singular', key: 'accS' },
            { label: 'Vocative Singular', key: 'vocS' },
            { label: 'Nominative Plural', key: 'nomP' },
            { label: 'Genitive Plural', key: 'genP' },
            { label: 'Dative Plural', key: 'datP' },
            { label: 'Accusative Plural', key: 'accP' },
            { label: 'Vocative Plural', key: 'vocP' }
        ]
    },
    adjective: {
        label: 'Adjective',
        inflections: [
            { label: 'Masculine Nominative Singular', key: 'mNomS' },
            { label: 'Feminine Nominative Singular', key: 'fNomS' },
            { label: 'Neuter Nominative Singular', key: 'nNomS' },
            { label: 'Masculine Accusative Singular', key: 'mAccS' },
            { label: 'Feminine Accusative Singular', key: 'fAccS' },
            { label: 'Neuter Accusative Singular', key: 'nAccS' }
        ]
    },
    adverb: {
        label: 'Adverb',
        inflections: [] // Adverbs don't have inflections
    },
    preposition: {
        label: 'Preposition',
        inflections: [] // Prepositions don't have inflections
    },
    conjunction: {
        label: 'Conjunction',
        inflections: [] // Conjunctions don't have inflections
    }
};

// Sentence construction state
let currentWord = '';
let currentFlashcard = null;

// Prolog session
let session;

// Initialize Prolog session
async function initializeProlog() {
    console.log('Starting Prolog initialization...');
    
    try {
        // Wait for Tau Prolog to be available
        if (typeof pl === 'undefined') {
            console.log('Waiting for Tau Prolog to load...');
            await new Promise((resolve, reject) => {
                let attempts = 0;
                const maxAttempts = 50; // 5 seconds maximum wait time
                
                const checkPl = setInterval(() => {
                    attempts++;
                    if (typeof pl !== 'undefined') {
                        clearInterval(checkPl);
                        console.log('Tau Prolog loaded successfully');
                        resolve();
                    } else if (attempts >= maxAttempts) {
                        clearInterval(checkPl);
                        reject(new Error('Tau Prolog failed to load after 5 seconds. Please check if the script is properly loaded.'));
                    }
                }, 100);
            });
        }
        
        console.log('Creating Prolog session...');
        session = pl.create();
        
        // Load grammar rules from external file
        console.log('Loading grammar rules from grammar.pl...');
        const response = await fetch('grammar.pl');
        if (!response.ok) {
            throw new Error(`Failed to load grammar.pl: ${response.statusText}`);
        }
        const grammarRules = await response.text();
        
        // Consult the grammar rules
        console.log('Consulting grammar rules...');
        session.consult(grammarRules);
        
        console.log('Prolog initialization completed successfully');
    } catch (error) {
        console.error('Error initializing Prolog:', error);
        // Show error to user
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = `Failed to initialize grammar checking: ${error.message}. Please refresh the page.`;
        document.querySelector('.sentence-section').prepend(errorMessage);
    }
}

async function checkGrammar() {
    console.log('Grammar check started');

    // Skip if Prolog session isn't ready yet
    if (!session) {
        console.log('Prolog session not ready yet');
        return;
    }

    // Get the words from the sentence blocks
    const blocks = Array.from(sentenceBlocks.querySelectorAll('.sentence-block'));
    const words = blocks
        .filter(block => block && block.querySelector('.block-text'))
        .map(block => `'${block.querySelector('.block-text').textContent}'`);

    // Skip if there are no words to check
    if (words.length === 0) {
        console.log('No words to check');
        return;
    }

    console.log('Words to check:', words);
    
    try {
        // Query the sentence
        console.log('About to query sentence...');
        session.query(`sentence([${words.join(', ')}]).`);
        session.answer(x => {
            if (x == false) {
                console.log('Sentence is invalid');
            } else {
                console.log('Sentence is valid');
            }
        });
        console.log('Query call completed');
    } catch (error) {
        console.error('Error in checkGrammar:', error);
    }
}

// Initialize DOM elements and event listeners
async function initializeApp() {
    // Get DOM elements
    flashcardContainer = document.getElementById('flashcardContainer');
    addFlashcardBtn = document.getElementById('addFlashcardBtn');
    flashcardForm = document.getElementById('flashcardForm');
    newFlashcardForm = document.getElementById('newFlashcardForm');
    cancelFlashcardBtn = document.getElementById('cancelFlashcard');
    wordTypeSelect = document.getElementById('wordType');
    inflectionFields = document.getElementById('inflectionFields');
    toggleFlashcardsBtn = document.getElementById('toggleFlashcards');
    prevCardBtn = document.getElementById('prevCard');
    nextCardBtn = document.getElementById('nextCard');
    cardCounter = document.getElementById('cardCounter');
    wordInput = document.getElementById('wordInput');
    wordSuggestions = document.getElementById('wordSuggestions');
    sentenceDisplay = document.getElementById('sentenceDisplay');
    sentenceBlocks = document.getElementById('sentenceBlocks');
    currentBlock = document.getElementById('currentBlock');
    blockInput = currentBlock.querySelector('.block-input');
    blockSuggestions = currentBlock.querySelector('.block-suggestions');
    flashcardSuggestion = document.getElementById('flashcardSuggestion');
    addNewFlashcardBtn = document.getElementById('addNewFlashcardBtn');

    // Add event listeners
    addFlashcardBtn.addEventListener('click', () => {
        flashcardForm.classList.remove('hidden');
        updateInflectionFields();
        flashcardForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    cancelFlashcardBtn.addEventListener('click', () => {
        flashcardForm.classList.add('hidden');
        newFlashcardForm.reset();
    });

    wordTypeSelect.addEventListener('change', updateInflectionFields);

    toggleFlashcardsBtn.addEventListener('click', () => {
        const content = document.querySelector('.flashcard-content');
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
        toggleFlashcardsBtn.textContent = content.style.display === 'none' ? '▼' : '▲';
    });

    prevCardBtn.addEventListener('click', () => {
        if (currentCardIndex > 0) {
            currentCardIndex--;
            displayCurrentCard();
        }
    });

    nextCardBtn.addEventListener('click', () => {
        if (currentCardIndex < flashcards.length - 1) {
            currentCardIndex++;
            displayCurrentCard();
        }
    });

    newFlashcardForm.addEventListener('submit', handleFlashcardSubmit);

    wordInput.addEventListener('input', handleWordInput);

    blockInput.addEventListener('focus', () => {
        displayBlockSuggestions(flashcards);
    });

    blockInput.addEventListener('input', handleBlockInput);

    blockInput.addEventListener('keydown', (e) => {
        if (e.key === ' ') {
            e.preventDefault(); // Prevent the space from being added to the input
            
            const currentWord = blockInput.value.trim();
            
            // Check if the word exists in flashcards
            const matches = flashcards.filter(card => {
                const matchesGreek = card.greek.toLowerCase() === currentWord.toLowerCase();
                const matchesInflections = Object.values(card.inflections).some(
                    inflection => inflection && inflection.toLowerCase() === currentWord.toLowerCase()
                );
                return matchesGreek || matchesInflections;
            });

            if (matches.length > 0) {
                // Word exists, create block and start new one
                const card = matches[0];
                // Find the matching inflection if it exists
                const matchingInflection = Object.values(card.inflections).find(
                    inflection => inflection && inflection.toLowerCase() === currentWord.toLowerCase()
                );
                createWordBlock(card, matchingInflection);
                blockInput.value = '';
                blockSuggestions.classList.remove('show');
                flashcardSuggestion.classList.add('hidden');
                // Show all options for the new block
                displayBlockSuggestions(flashcards);
                // Check grammar after adding the new word
                checkGrammar();
            } else if (currentWord !== '') {
                // Word doesn't exist, show suggestion to add new flashcard
                flashcardSuggestion.classList.remove('hidden');
            }
        } else if (e.key === 'Backspace' || e.key === 'Delete') {
            // If the input is empty and there are blocks before the current block, remove the last block
            if (blockInput.value === '') {
                const blocks = Array.from(sentenceBlocks.querySelectorAll('.sentence-block'));
                const currentBlockIndex = blocks.findIndex(block => block === currentBlock);
                if (currentBlockIndex > 0) {
                    const lastBlock = blocks[currentBlockIndex - 1];
                    lastBlock.remove();
                    checkGrammar();
                }
            }
            // Otherwise, let the default backspace/delete behavior handle deleting the last character
        }
    });

    blockSuggestions.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    document.addEventListener('click', (e) => {
        if (!blockInput.contains(e.target) && !blockSuggestions.contains(e.target)) {
            blockSuggestions.classList.remove('show');
        }
    });

    addNewFlashcardBtn.addEventListener('click', handleAddNewFlashcard);

    // Load initial data
    loadFlashcards();
    displayCurrentCard();

    // Initialize Prolog
    await initializeProlog();
}

// Event handler functions
function handleFlashcardSubmit(e) {
    e.preventDefault();
    console.log('Form submitted');
    
    const formData = new FormData(newFlashcardForm);
    const flashcard = {
        type: formData.get('wordType'),
        greek: formData.get('greekWord'),
        english: formData.get('englishTranslation'),
        inflections: {}
    };

    console.log('Flashcard data:', flashcard);

    if (wordTypeConfigs[flashcard.type] && wordTypeConfigs[flashcard.type].inflections.length > 0) {
        wordTypeConfigs[flashcard.type].inflections.forEach(inflection => {
            flashcard.inflections[inflection.key] = formData.get(inflection.key);
        });
    }

    console.log('Flashcard with inflections:', flashcard);

    flashcards.push(flashcard);
    saveFlashcards();
    console.log('Flashcards saved:', flashcards);
    
    flashcardForm.classList.add('hidden');
    newFlashcardForm.reset();
    displayCurrentCard();
    showSaveIndicator('Flashcard saved successfully');
}

function handleWordInput(e) {
    const input = e.target.value.trim();
    if (input === '') {
        wordSuggestions.style.display = 'none';
        return;
    }

    const suggestions = flashcards.filter(card => 
        card.greek.toLowerCase().includes(input.toLowerCase()) ||
        card.english.toLowerCase().includes(input.toLowerCase())
    );

    displaySuggestions(suggestions);
}

function handleBlockInput(e) {
    currentWord = e.target.value.trim();
    
    // If input is empty, show all flashcards
    if (currentWord === '') {
        displayBlockSuggestions(flashcards);
        flashcardSuggestion.classList.add('hidden');
        return;
    }
    
    // Normal input handling for non-empty input
    const matches = flashcards.filter(card => {
        const matchesGreek = card.greek.toLowerCase().startsWith(currentWord.toLowerCase());
        const matchesInflections = Object.values(card.inflections).some(
            inflection => inflection && inflection.toLowerCase().startsWith(currentWord.toLowerCase())
        );
        return matchesGreek || matchesInflections;
    });

    displayBlockSuggestions(matches);
    flashcardSuggestion.classList.add('hidden');
}

function handleAddNewFlashcard() {
    const wordToAdd = currentWord;
    flashcardForm.classList.remove('hidden');
    updateInflectionFields();
    document.getElementById('greekWord').value = wordToAdd;
    flashcardForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    flashcardSuggestion.classList.add('hidden');
}

// Load flashcards from localStorage when the page loads
function loadFlashcards() {
    const savedFlashcards = localStorage.getItem(STORAGE_KEY);
    if (savedFlashcards) {
        flashcards = JSON.parse(savedFlashcards);
        displayCurrentCard();
    }
}

// Save flashcards to localStorage
function saveFlashcards() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(flashcards));
}

// Functions
function updateInflectionFields() {
    const wordType = wordTypeSelect.value;
    inflectionFields.innerHTML = '';

    if (wordType && wordTypeConfigs[wordType]) {
        switch (wordType) {
            case 'verb':
                // Create table for verb inflections
                const verbTable = document.createElement('table');
                verbTable.className = 'inflection-table';
                verbTable.innerHTML = `
                    <thead>
                        <tr>
                            <th colspan="3">Active Present Indicative</th>
                        </tr>
                        <tr>
                            <th>Person</th>
                            <th>Singular</th>
                            <th>Plural</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1st</td>
                            <td><input type="text" id="present1s" name="present1s" required></td>
                            <td><input type="text" id="present1p" name="present1p" required></td>
                        </tr>
                        <tr>
                            <td>2nd</td>
                            <td><input type="text" id="present2s" name="present2s" required></td>
                            <td><input type="text" id="present2p" name="present2p" required></td>
                        </tr>
                        <tr>
                            <td>3rd</td>
                            <td><input type="text" id="present3s" name="present3s" required></td>
                            <td><input type="text" id="present3p" name="present3p" required></td>
                        </tr>
                    </tbody>
                `;
                inflectionFields.appendChild(verbTable);
                break;

            case 'noun':
                // Create table for noun inflections
                const nounTable = document.createElement('table');
                nounTable.className = 'inflection-table';
                nounTable.innerHTML = `
                    <thead>
                        <tr>
                            <th></th>
                            <th colspan="2">Declension</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Singular</th>
                            <th>Plural</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Nom</td>
                            <td><input type="text" id="nomS" name="nomS" required></td>
                            <td><input type="text" id="nomP" name="nomP" required></td>
                        </tr>
                        <tr>
                            <td>Gen</td>
                            <td><input type="text" id="genS" name="genS" required></td>
                            <td><input type="text" id="genP" name="genP" required></td>
                        </tr>
                        <tr>
                            <td>Dat</td>
                            <td><input type="text" id="datS" name="datS" required></td>
                            <td><input type="text" id="datP" name="datP" required></td>
                        </tr>
                        <tr>
                            <td>Acc</td>
                            <td><input type="text" id="accS" name="accS" required></td>
                            <td><input type="text" id="accP" name="accP" required></td>
                        </tr>
                        <tr>
                            <td>Voc</td>
                            <td><input type="text" id="vocS" name="vocS" required></td>
                            <td><input type="text" id="vocP" name="vocP" required></td>
                        </tr>
                    </tbody>
                `;
                inflectionFields.appendChild(nounTable);
                break;

            case 'adjective':
                // Create table for adjective inflections
                const adjTable = document.createElement('table');
                adjTable.className = 'inflection-table';
                adjTable.innerHTML = `
                    <thead>
                        <tr>
                            <th></th>
                            <th colspan="2">Declension</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>Singular</th>
                            <th>Plural</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Nom</td>
                            <td><input type="text" id="nomS" name="nomS" required></td>
                            <td><input type="text" id="nomP" name="nomP" required></td>
                        </tr>
                        <tr>
                            <td>Gen</td>
                            <td><input type="text" id="genS" name="genS" required></td>
                            <td><input type="text" id="genP" name="genP" required></td>
                        </tr>
                        <tr>
                            <td>Dat</td>
                            <td><input type="text" id="datS" name="datS" required></td>
                            <td><input type="text" id="datP" name="datP" required></td>
                        </tr>
                        <tr>
                            <td>Acc</td>
                            <td><input type="text" id="accS" name="accS" required></td>
                            <td><input type="text" id="accP" name="accP" required></td>
                        </tr>
                        <tr>
                            <td>Voc</td>
                            <td><input type="text" id="vocS" name="vocS" required></td>
                            <td><input type="text" id="vocP" name="vocP" required></td>
                        </tr>
                    </tbody>
                `;
                inflectionFields.appendChild(adjTable);
                break;

            case 'adverb':
            case 'preposition':
            case 'conjunction':
                // These types don't have inflections, so we'll just show a message
                inflectionFields.innerHTML = '<p class="no-inflections">This word type does not have inflections.</p>';
                break;
        }
    }
}

function createFlashcardElement(flashcard) {
    const div = document.createElement('div');
    div.className = 'flashcard';
    div.setAttribute('data-type', flashcard.type);
    div.innerHTML = `
        <div class="flashcard-inner">
            <div class="flashcard-front">
                <div class="flashcard-content">
                    <div class="main-word">${flashcard.greek}</div>
                    <div class="inflections-preview">
                        ${Object.values(flashcard.inflections).join(', ')}
                    </div>
                </div>
                <button class="delete-btn" title="Delete flashcard">×</button>
            </div>
            <div class="flashcard-back">
                <div class="flashcard-content">
                    <div class="main-word">${flashcard.english}</div>
                </div>
                <button class="delete-btn" title="Delete flashcard">×</button>
            </div>
        </div>
    `;

    // Add click event for flipping
    div.addEventListener('click', (e) => {
        // Don't flip if clicking the delete button
        if (!e.target.classList.contains('delete-btn')) {
            div.classList.toggle('flipped');
        }
    });

    // Add delete button functionality
    const deleteBtn = div.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent card flip when clicking delete
        if (confirm('Are you sure you want to delete this flashcard?')) {
            const index = flashcards.findIndex(card => 
                card.greek === flashcard.greek && 
                card.english === flashcard.english
            );
            if (index !== -1) {
                flashcards.splice(index, 1);
                saveFlashcards();
                displayCurrentCard();
                showSaveIndicator('Flashcard deleted');
            }
        }
    });

    return div;
}

function displayCurrentCard() {
    flashcardContainer.innerHTML = '';
    if (flashcards.length > 0) {
        const card = createFlashcardElement(flashcards[currentCardIndex]);
        flashcardContainer.appendChild(card);
        cardCounter.textContent = `${currentCardIndex + 1}/${flashcards.length}`;
    } else {
        cardCounter.textContent = '0/0';
    }
}

function displaySuggestions(suggestions) {
    wordSuggestions.innerHTML = '';
    if (suggestions.length > 0) {
        suggestions.forEach(card => {
            const div = document.createElement('div');
            div.className = 'word-suggestion';
            div.textContent = `${card.greek} (${card.english})`;
            div.addEventListener('click', () => {
                addWordToSentence(card);
                wordInput.value = '';
                wordSuggestions.style.display = 'none';
            });
            wordSuggestions.appendChild(div);
        });
        wordSuggestions.style.display = 'block';
    } else {
        wordSuggestions.style.display = 'none';
    }
}

function addWordToSentence(flashcard) {
    const wordSpan = document.createElement('span');
    wordSpan.textContent = flashcard.greek;
    wordSpan.className = 'sentence-word';
    wordSpan.setAttribute('data-type', flashcard.type);
    wordSpan.addEventListener('click', () => {
        // Show the corresponding flashcard
        const index = flashcards.findIndex(card => card.greek === flashcard.greek);
        if (index !== -1) {
            currentCardIndex = index;
            displayCurrentCard();
        }
    });
    sentenceDisplay.appendChild(wordSpan);
    sentenceDisplay.appendChild(document.createTextNode(' '));
}

function showSaveIndicator(message) {
    const indicator = document.createElement('div');
    indicator.className = 'save-indicator';
    indicator.textContent = message;
    document.body.appendChild(indicator);

    // Remove the indicator after 2 seconds
    setTimeout(() => {
        indicator.remove();
    }, 2000);
}

function createWordBlock(flashcard, selectedInflection = null) {
    const block = document.createElement('div');
    block.className = 'sentence-block';
    block.setAttribute('data-type', flashcard.type);
    block.setAttribute('draggable', 'true');
    
    // Add styles for the remove button
    const style = document.createElement('style');
    style.textContent = `
        .sentence-block {
            position: relative;
        }
        .remove-word {
            position: absolute;
            top: 2px;
            right: 2px;
            width: 20px;
            height: 20px;
            line-height: 18px;
            text-align: center;
            background: none;
            border: none;
            color: #666;
            cursor: pointer;
            font-size: 16px;
            padding: 0;
            border-radius: 50%;
            display: none;
        }
        .sentence-block:hover .remove-word {
            display: block;
        }
        .remove-word:hover {
            background-color: #ff4444;
            color: white;
        }
    `;
    document.head.appendChild(style);
    
    // Use the selected inflection if provided, otherwise use the main word
    const displayText = selectedInflection || flashcard.greek;
    block.innerHTML = `
        <span class="block-text">${displayText}</span>
        <button class="remove-word" title="Remove word">×</button>
    `;

    // Add remove button functionality
    const removeBtn = block.querySelector('.remove-word');
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent drag and drop when clicking remove
        block.remove();
        checkGrammar();
    });

    // Add drag and drop functionality
    block.addEventListener('dragstart', (e) => {
        block.classList.add('dragging');
        e.dataTransfer.setData('text/plain', '');
    });

    block.addEventListener('dragend', () => {
        block.classList.remove('dragging');
        checkGrammar(); // Check grammar after reordering
    });

    block.addEventListener('dragover', (e) => {
        e.preventDefault();
        const draggingBlock = document.querySelector('.dragging');
        if (draggingBlock && draggingBlock !== block) {
            const rect = block.getBoundingClientRect();
            const midY = rect.top + rect.height / 2;
            if (e.clientY < midY) {
                block.parentNode.insertBefore(draggingBlock, block);
            } else {
                block.parentNode.insertBefore(draggingBlock, block.nextSibling);
            }
        }
    });

    // Insert before the current block
    currentBlock.parentNode.insertBefore(block, currentBlock);
    
    // Wait for the next tick to ensure the block is fully rendered
    setTimeout(() => {
        checkGrammar();
    }, 0);
}

function displayBlockSuggestions(matches) {
    blockSuggestions.innerHTML = '';
    
    // Show all words with their inflections
    matches.forEach(card => {
        // Add main word
        const mainDiv = document.createElement('div');
        mainDiv.className = 'suggestion-item';
        mainDiv.textContent = `${card.greek} (${card.english})`;
        mainDiv.addEventListener('click', () => {
            currentFlashcard = card;
            blockInput.value = card.greek;
            blockSuggestions.classList.remove('show');
            createWordBlock(card);
            blockInput.value = ''; // Clear the input after creating the block
        });
        blockSuggestions.appendChild(mainDiv);

        // Add inflections
        Object.entries(card.inflections).forEach(([key, inflection]) => {
            if (inflection) {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                const inflectionLabel = wordTypeConfigs[card.type].inflections.find(i => i.key === key)?.label || key;
                div.textContent = `${inflection} (${card.greek} - ${inflectionLabel})`;
                div.addEventListener('click', () => {
                    currentFlashcard = card;
                    blockInput.value = inflection;
                    blockSuggestions.classList.remove('show');
                    createWordBlock(card, inflection);
                    blockInput.value = ''; // Clear the input after creating the block
                });
                blockSuggestions.appendChild(div);
            }
        });
    });

    // Show the suggestions container
    blockSuggestions.classList.add('show');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp); 