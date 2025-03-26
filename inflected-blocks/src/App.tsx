import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Container, AppBar, Toolbar, Typography, Box, Tabs, Tab } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import WordForm from './components/WordForm';
import WordList from './components/WordList';
import FlashcardReview from './components/FlashcardReview';
import SentenceBuilder from './components/SentenceBuilder';
import { Word } from './types/word';
import { getWords, saveWords } from './utils/wordStorage';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [editingWord, setEditingWord] = useState<Word | undefined>();
  const [currentTab, setCurrentTab] = useState(0);
  const [words, setWords] = useState<Word[]>(getWords());

  useEffect(() => {
    saveWords(words);
  }, [words]);

  const handleEdit = (word: Word) => {
    setEditingWord(word);
  };

  const handleCancelEdit = () => {
    setEditingWord(undefined);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  const handleWordUpdate = (updatedWords: Word[]) => {
    setWords(updatedWords);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Inflected Blocks
              </Typography>
            </Toolbar>
          </AppBar>
          <Container maxWidth="md" sx={{ mt: 4 }}>
            <Routes>
              <Route path="/" element={
                <>
                  <Typography variant="h4" component="h1" gutterBottom>
                    Welcome to Inflected Blocks
                  </Typography>
                  <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                    <Tabs value={currentTab} onChange={handleTabChange}>
                      <Tab label="Manage Words" />
                      <Tab label="Review" />
                      <Tab label="Build Sentences" />
                    </Tabs>
                  </Box>
                  {currentTab === 0 ? (
                    <>
                      <WordForm
                        wordToEdit={editingWord}
                        onCancel={handleCancelEdit}
                        onWordUpdate={handleWordUpdate}
                      />
                      <WordList 
                        onEdit={handleEdit} 
                        onWordUpdate={handleWordUpdate}
                      />
                    </>
                  ) : currentTab === 1 ? (
                    <FlashcardReview words={words} />
                  ) : (
                    <SentenceBuilder words={words} />
                  )}
                </>
              } />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
