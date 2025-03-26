import React, { useState, useEffect } from 'react';
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
import { saveWord, updateWord } from '../utils/wordStorage';
import { notifyWordUpdates } from '../utils/events';

interface WordFormProps {
  wordToEdit?: Word;
  onCancel?: () => void;
}

export default function WordForm({ wordToEdit, onCancel }: WordFormProps) {
  const [word, setWord] = useState<Word>({
    lemma: '',
    translation: '',
    inflections: [{ form: '', description: '' }],
  });
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    if (wordToEdit) {
      setWord(wordToEdit);
    }
  }, [wordToEdit]);

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
    if (wordToEdit) {
      updateWord(wordToEdit, word);
    } else {
      saveWord(word);
    }
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
        {wordToEdit ? 'Edit Word' : 'Add New Word'}
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
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button type="submit" variant="contained" color="primary">
              {wordToEdit ? 'Update Word' : 'Save Word'}
            </Button>
            {onCancel && (
              <Button onClick={onCancel} variant="outlined">
                Cancel
              </Button>
            )}
          </Box>
        </Stack>
      </form>
      <Snackbar
        open={showSuccess}
        autoHideDuration={3000}
        onClose={() => setShowSuccess(false)}
      >
        <Alert onClose={() => setShowSuccess(false)} severity="success">
          {wordToEdit ? 'Word updated successfully!' : 'Word saved successfully!'}
        </Alert>
      </Snackbar>
    </Paper>
  );
} 