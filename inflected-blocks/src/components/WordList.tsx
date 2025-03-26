import React, { useEffect, useState } from 'react';
import {
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Button,
  Divider,
  Box,
} from '@mui/material';
import { Word } from '../types/word';
import { getWords, deleteWord } from '../utils/wordStorage';
import { subscribeToWordUpdates } from '../utils/events';

interface WordListProps {
  onEdit: (word: Word) => void;
  onWordUpdate: (words: Word[]) => void;
}

export default function WordList({ onEdit, onWordUpdate }: WordListProps) {
  const [words, setWords] = useState<Word[]>([]);

  useEffect(() => {
    setWords(getWords());
    const unsubscribe = subscribeToWordUpdates(() => {
      setWords(getWords());
    });
    return unsubscribe;
  }, []);

  const handleDelete = (index: number) => {
    deleteWord(index);
    const updatedWords = getWords();
    setWords(updatedWords);
    onWordUpdate(updatedWords);
  };

  if (words.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="body1" color="text.secondary">
          No words saved yet. Add some words using the form above!
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Saved Words
      </Typography>
      <List>
        {words.map((word, index) => (
          <React.Fragment key={index}>
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
                    {word.inflections.map((inflection, i) => (
                      <Typography
                        key={i}
                        variant="body2"
                        component="div"
                        sx={{ display: 'flex', gap: 2 }}
                      >
                        <Typography component="span" sx={{ fontWeight: 'bold' }}>
                          {inflection.form}
                        </Typography>
                        <Typography component="span" color="text.secondary">
                          {inflection.description}
                        </Typography>
                      </Typography>
                    ))}
                  </Box>
                }
              />
              <ListItemSecondaryAction>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    onClick={() => onEdit(word)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="outlined"
                    color="error"
                    onClick={() => handleDelete(index)}
                  >
                    Delete
                  </Button>
                </Box>
              </ListItemSecondaryAction>
            </ListItem>
            {index < words.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </List>
    </Paper>
  );
} 