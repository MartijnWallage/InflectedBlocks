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

// Menu
let database = 'grammar.pl';

const menu = document.getElementById('menu');

const openButton = document.getElementById('open-button');
openButton.onclick = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.pl';
  input.onchange = (e) => {
    const file = e.target.files[0];
    database = file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
      const databaseString = e.target.result;
      consultDatabase(databaseString);
    };
    reader.readAsText(file);
  };
  input.click();
};

const saveButton = document.getElementById('save-button');
saveButton.onclick = () => {
  const databaseString = session.toString();
  const blob = new Blob([databaseString], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = database;
  a.click();
  URL.revokeObjectURL(url);
};

// Add event listener to toggle menu dropdown
const menuButton = menu.querySelector('.menu-button');
menuButton.addEventListener('click', () => {
  const menuDropdown = menu.querySelector('.menu-dropdown');
  menuDropdown.classList.toggle('show');
});


async function consultDatabase(db) {
    session.consult(db);
    loadFlashcardsFromProlog();
}


// Function to create flashcards from the Prolog database
function loadFlashcardsFromProlog() {
    console.log('Creating flashcards from Prolog...');
    console.log(session.toString());

    // Query the Prolog database for all words and their types
    session.query("word_type(X, Y).", {
        success: (goal) => {
            console.log(`Query parsed: ${goal}.`);
            
            // Collect all answers first
            let allAnswers = [];
            function collectAnswers() {
                session.answer({
                    success: (answer) => {
                        console.log(`Answer received: ${answer}.`);
                        const formattedAnswer = session.format_answer(answer);
                        console.log(`Formatted answer: ${formattedAnswer}`);
                        allAnswers.push(formattedAnswer);
                        collectAnswers();
                    },
                    error: (error) => {
                        console.error(`Error getting answer: ${error}.`);
                        collectAnswers();
                    },
                    fail: () => {
                        console.log('No more answers available.');
                        console.log('All answers collected:', allAnswers);
                        // Now process all answers
                        processAllAnswers(allAnswers);
                    }
                });
            }

            // Process all collected answers
            function processAllAnswers(answers) {
                console.log('Processing all answers...');
                answers.forEach(answer => {
                    createFlashcardFromProlog(answer);
                });
            }

            // Start collecting answers
            console.log('Starting to collect answers...');
            collectAnswers();
        },
        error: (error) => {
            console.error(`Error in initial query: ${error}.`);
        }
    });
}

function createFlashcardFromProlog(answer) {
    console.log('Creating flashcard from answer:', answer);
    const parts = answer.split(", ");
    const xPart = parts[0];
    const yPart = parts[1];

    const greek = xPart.split(" = ")[1];
    const type = yPart.split(" = ")[1];

    console.log(`Creating flashcard for word: ${greek} of type: ${type}`);

    const flashcard = {
        type: type,
        greek: greek,
        english: '',
        inflections: {}
    };

    // Query the Prolog database for the word's translation
    session.query(`word_translation('${flashcard.greek}', X).`, {
        success: (goal) => {
            console.log(`Translation query parsed for ${flashcard.greek}`);
            session.answer({
                success: (translationAnswer) => {
                    const translationString = session.format_answer(translationAnswer);
                    flashcard.english = translationString.split(" = ")[1];
                    console.log(`Got translation: ${flashcard.english}`);

                    // If the word is a verb, query the Prolog database for its inflections
                    if (flashcard.type === 'verb') {
                        session.query(`word_inflection('${flashcard.greek}', X, Y).`, {
                            success: (inflectionGoal) => {
                                console.log(`Inflection query parsed for ${flashcard.greek}`);
                                function getInflections() {
                                    session.answer({
                                        success: (inflectionAnswer) => {
                                            const inflectionString = session.format_answer(inflectionAnswer);
                                            const inflectionParts = inflectionString.split(", ");
                                            const inflectionTypePart = inflectionParts[0];
                                            const inflectionFormPart = inflectionParts[1];
                                            const inflectionType = inflectionTypePart.split(" = ")[1];
                                            const inflectionForm = inflectionFormPart.split(" = ")[1];
                                            flashcard.inflections[inflectionType] = inflectionForm;
                                            console.log(`Got inflection: ${inflectionType} = ${inflectionForm}`);
                                            getInflections();
                                        },
                                        error: (error) => {
                                            console.error(`Error getting inflection: ${error}.`);
                                            finishFlashcard();
                                        },
                                        fail: () => {
                                            console.log('No more inflections.');
                                            finishFlashcard();
                                        }
                                    });
                                }
                                getInflections();
                            },
                            error: (error) => {
                                console.error(`Error querying inflections: ${error}.`);
                                finishFlashcard();
                            }
                        });
                    } else {
                        finishFlashcard();
                    }
                },
                error: (error) => {
                    console.error(`Error getting translation: ${error}.`);
                    finishFlashcard();
                },
                fail: () => {
                    console.log('No translation found.');
                    finishFlashcard();
                }
            });
        },
        error: (error) => {
            console.error(`Error querying translation: ${error}.`);
            finishFlashcard();
        }
    });

    function finishFlashcard() {
        console.log('Finishing flashcard:', flashcard);
        flashcards.push(flashcard);
        displayCurrentCard();
    }
}

function initializeProlog() {
	session = pl.create(1000);

	consultDatabase(database);
}


function assertWord(word, type) {
	let assertion = `asserta(word_type('${word}', ${type})).`;
	session.query(assertion, {
        success: function(goal) {
            console.log(`Query parsed: ${goal}.`);
            session.answer({
                success: function (answer) {
                    console.log(`${assertion} is ${answer}`);
                },
                error: function (err) {
                    console.log(`Error: ${err}.`);
                },
                fail: function (fail) {
                    console.log(`${assertion} is ${fail}.`);
                },
                limit: function () {
                    console.log('Limit exceeded.');
                },
            });
        },
        error: function(err) {
            console.log(`Query parsing error: ${err}.`);
        }
    });
}

function isValidSentence(wordsArray) {
	let prologList = `[${wordsArray.map(w => `'${w}'`).join(', ')}]`;
	console.log(`Checking if ${prologList} is a valid sentence...`);
	let query = `valid_sentence(${prologList}).`;

    return new Promise((resolve, reject) => {
            session.query(query, {
                success: function(goal) {
                    console.log(`Query parsed: ${goal}.`);
                    session.answer({
                        success: function (answer) {
                            console.log(`${query} is ${answer}`);
                            resolve(true);
                        },
                        error: function (err) {
                            console.log(`Error: ${err}.`);
                            resolve(false);
                        },
                        fail: function (fail) {
                            console.log(`${query} is ${fail}.`);
                            resolve(false);
                        },
                        limit: function () {
                            console.log('Limit exceeded.')
                            resolve(false);
                        },
                    });
                },
                error: function(err) {
                    console.log(`Query parsing error: ${err}.`);
                    resolve(false);
                }
            });
        });
}


function checkGrammar() {
    console.log('Grammar check started');

    // Skip if Prolog session isn't ready yet
    if (!session) {
        console.log('Prolog session not ready yet');
        return;
    }
	console.log(`Prolog session ready: ${session}`);

    // Get the words from the sentence blocks
    const blocks = Array.from(sentenceBlocks.querySelectorAll('.sentence-block'));
    const words = blocks
        .filter(block => block && block.querySelector('.block-text'))
        .map(block => {
    const wordElement = block.querySelector('.block-text');
    const word = wordElement.textContent;
    const type = block.getAttribute('data-type');
    const flashcard = flashcards.find(card => 
        card.greek === word || Object.values(card.inflections).includes(word)
    );

    if (flashcard) {
        // Find the matching inflection if it exists
        const matchingInflection = Object.entries(flashcard.inflections).find(([key, inflection]) => inflection === word);
    }

        return `${word}`;
    });

    // Skip if there are no words to check
    if (words.length === 0) {
        console.log('No words to check');
        return;
    }

    console.log('Words to check:', words);
    
    // Query the sentence
    console.log('About to query sentence...', words);
    isValidSentence(words).then((isValid) => {
        if (isValid) {
            sentenceBlocks.style.border = '2px solid green';
        } else {
            sentenceBlocks.style.border = '2px solid red';
        }
    });
}

// Initialize DOM elements and event listeners
function initializeApp() {

    // Initialize Prolog
    initializeProlog();

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
  //  loadFlashcards();
    displayCurrentCard();

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

    assertWord(flashcard.greek, flashcard.type);

    console.log('Flashcard data:', flashcard);

    if (wordTypeConfigs[flashcard.type] && wordTypeConfigs[flashcard.type].inflections.length > 0) {
        wordTypeConfigs[flashcard.type].inflections.forEach(inflection => {
            flashcard.inflections[inflection.key] = formData.get(inflection.key);
            assertWord(flashcard.inflections[inflection.key], flashcard.type);
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