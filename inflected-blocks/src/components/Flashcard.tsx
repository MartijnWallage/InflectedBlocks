import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Stack,
  Chip,
} from '@mui/material';
import { Word, WordType } from '../types/word';

interface FlashcardProps {
  word: Word;
  isFlipped: boolean;
  onFlip: () => void;
}

const getWordTypeColor = (wordType: WordType) => {
  switch (wordType) {
    case WordType.Verb:
      return '#1976d2'; // Blue
    case WordType.Noun:
      return '#2e7d32'; // Green
    case WordType.Adjective:
      return '#ed6c02'; // Orange
    case WordType.Adverb:
      return '#9c27b0'; // Purple
    case WordType.Conjunction:
      return '#d32f2f'; // Red
    case WordType.Preposition:
      return '#0288d1'; // Light Blue
    case WordType.Pronoun:
      return '#7b1fa2'; // Deep Purple
    case WordType.Article:
      return '#455a64'; // Blue Grey
    default:
      return '#757575'; // Grey
  }
};

export default function Flashcard({ word, isFlipped, onFlip }: FlashcardProps) {
  const wordTypeColor = getWordTypeColor(word.wordType);

  return (
    <Paper
      elevation={3}
      sx={{
        p: 4,
        minHeight: '300px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        cursor: 'pointer',
        perspective: '1000px',
        transformStyle: 'preserve-3d',
        transition: 'transform 0.6s',
        transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0)',
        position: 'relative',
        borderTop: `4px solid ${wordTypeColor}`,
      }}
      onClick={onFlip}
    >
      <Box
        sx={{
          backfaceVisibility: 'hidden',
          width: '100%',
        }}
      >
        <Stack spacing={2}>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
            <Typography variant="h4" component="div" align="center">
              {word.lemma}
            </Typography>
            <Chip
              label={word.wordType}
              size="small"
              sx={{
                backgroundColor: wordTypeColor,
                color: 'white',
                '& .MuiChip-label': {
                  textTransform: 'capitalize',
                },
              }}
            />
          </Box>
          <Box>
            {word.inflections.map((inflection, index) => (
              <Typography
                key={index}
                variant="h6"
                component="div"
                align="center"
                sx={{ mb: 1 }}
              >
                <Typography component="span" sx={{ fontWeight: 'bold' }}>
                  {inflection.form}
                </Typography>
                <Typography
                  component="span"
                  color="text.secondary"
                  sx={{ ml: 1 }}
                >
                  {inflection.description}
                </Typography>
              </Typography>
            ))}
          </Box>
        </Stack>
      </Box>
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          p: 4,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backfaceVisibility: 'hidden',
          transform: 'rotateY(180deg)',
          backgroundColor: 'background.paper',
        }}
      >
        <Typography variant="h4" component="div" align="center">
          {word.translation}
        </Typography>
      </Box>
    </Paper>
  );
} 