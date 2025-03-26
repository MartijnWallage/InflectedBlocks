import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Stack,
  Snackbar,
  Alert,
} from '@mui/material';
import { Word, Inflection } from '../types/word';
import { saveWord } from '../utils/wordStorage';
import { notifyWordUpdates } from '../utils/events';

export default function WordForm() {
  const [word, setWord] = useState<Word>({
    lemma: '',
    translation: '',
    inflections: [{ form: '', description: '' }],
  });
  const [showSuccess, setShowSuccess] = useState(false);

  const handleAddInflection = () => {
    setWord({
      ...word,
      inflections: [...word.inflections, { form: '', description: '' }],
    });
  };

  const handleRemoveInflection = (index: number) => {
    setWord({
      ...word,
      inflections: word.inflections.filter((_, i) => i !== index),
    });
  };

  const handleInflectionChange = (
    index: number,
    field: keyof Inflection,
    value: string
  ) => {
    const newInflections = [...word.inflections];
    newInflections[index] = { ...newInflections[index], [field]: value };
    setWord({ ...word, inflections: newInflections });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    saveWord(word);
    setWord({
      lemma: '',
      translation: '',
      inflections: [{ form: '', description: '' }],
    });
    setShowSuccess(true);
    notifyWordUpdates();
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Add New Word
      </Typography>
      <form onSubmit={handleSubmit}>
        <Stack spacing={3}>
          <TextField
            label="Lemma"
            value={word.lemma}
            onChange={(e) => setWord({ ...word, lemma: e.target.value })}
            fullWidth
            required
          />
          <TextField
            label="Translation"
            value={word.translation}
            onChange={(e) => setWord({ ...word, translation: e.target.value })}
            fullWidth
            required
          />
          
          <Typography variant="subtitle1" gutterBottom>
            Inflections
          </Typography>
          
          {word.inflections.map((inflection, index) => (
            <Box key={index} sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <TextField
                label="Form"
                value={inflection.form}
                onChange={(e) =>
                  handleInflectionChange(index, 'form', e.target.value)
                }
                fullWidth
                required
              />
              <TextField
                label="Description"
                value={inflection.description}
                onChange={(e) =>
                  handleInflectionChange(index, 'description', e.target.value)
                }
                fullWidth
                required
              />
              {word.inflections.length > 1 && (
                <Button
                  onClick={() => handleRemoveInflection(index)}
                  color="error"
                  variant="outlined"
                >
                  Remove
                </Button>
              )}
            </Box>
          ))}
          
          <Button
            onClick={handleAddInflection}
            variant="outlined"
          >
            Add Inflection
          </Button>
          
          <Button type="submit" variant="contained" color="primary">
            Save Word
          </Button>
        </Stack>
      </form>
      <Snackbar
        open={showSuccess}
        autoHideDuration={3000}
        onClose={() => setShowSuccess(false)}
      >
        <Alert onClose={() => setShowSuccess(false)} severity="success">
          Word saved successfully!
        </Alert>
      </Snackbar>
    </Paper>
  );
} 