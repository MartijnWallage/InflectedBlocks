import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Stack,
} from '@mui/material';
import { Word } from '../types/word';

interface FlashcardProps {
  word: Word;
  isFlipped: boolean;
  onFlip: () => void;
}

export default function Flashcard({ word, isFlipped, onFlip }: FlashcardProps) {
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
          <Typography variant="h4" component="div" align="center">
            {word.lemma}
          </Typography>
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