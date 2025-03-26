import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Stack,
  Chip,
} from '@mui/material';
import { Word } from '../types/word';

interface SentenceBuilderProps {
  words: Word[];
}

export default function SentenceBuilder({ words }: SentenceBuilderProps) {
  const [selectedWords, setSelectedWords] = useState<Array<{ word: Word; inflection: string }>>([]);
  const [sentence, setSentence] = useState<string>('');

  const handleWordSelect = (word: Word, inflection: string) => {
    setSelectedWords([...selectedWords, { word, inflection }]);
    setSentence(prev => prev + (prev ? ' ' : '') + inflection);
  };

  const handleRemoveWord = (index: number) => {
    const newSelectedWords = selectedWords.filter((_, i) => i !== index);
    setSelectedWords(newSelectedWords);
    setSentence(newSelectedWords.map(w => w.inflection).join(' '));
  };

  const handleClear = () => {
    setSelectedWords([]);
    setSentence('');
  };

  const handleCheckSentence = () => {
    // TODO: Integrate with SWI-Prolog for grammatical validation
    console.log('Checking sentence:', sentence);
  };

  if (words.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="body1" color="text.secondary">
          No words available. Add some words first!
        </Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Construct Your Sentence
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1" gutterBottom>
            Current sentence:
          </Typography>
          <Typography variant="h5" component="div" sx={{ mb: 2 }}>
            {sentence || 'No words selected'}
          </Typography>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            {selectedWords.map((selected, index) => (
              <Chip
                key={index}
                label={selected.inflection}
                onDelete={() => handleRemoveWord(index)}
                color="primary"
                variant="outlined"
              />
            ))}
          </Stack>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              onClick={handleCheckSentence}
              disabled={!sentence}
            >
              Check Sentence
            </Button>
            <Button
              variant="outlined"
              onClick={handleClear}
              disabled={!sentence}
            >
              Clear
            </Button>
          </Box>
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Available Words
        </Typography>
        <List>
          {words.map((word, wordIndex) => (
            <React.Fragment key={wordIndex}>
              <ListItem>
                <ListItemText
                  primary={
                    <Box>
                      <Typography variant="subtitle1" component="span">
                        {word.lemma}
                      </Typography>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        component="span"
                        sx={{ ml: 1 }}
                      >
                        ({word.translation})
                      </Typography>
                    </Box>
                  }
                  secondary={
                    <Box sx={{ mt: 1 }}>
                      {word.inflections.map((inflection, inflectionIndex) => (
                        <Button
                          key={inflectionIndex}
                          variant="outlined"
                          size="small"
                          sx={{ mr: 1, mb: 1 }}
                          onClick={() => handleWordSelect(word, inflection.form)}
                        >
                          {inflection.form}
                        </Button>
                      ))}
                    </Box>
                  }
                />
              </ListItem>
              {wordIndex < words.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    </Box>
  );
} 