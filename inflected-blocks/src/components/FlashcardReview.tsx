import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
} from '@mui/material';
import { Word } from '../types/word';
import Flashcard from './Flashcard';

interface FlashcardReviewProps {
  words: Word[];
}

export default function FlashcardReview({ words }: FlashcardReviewProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const handleNext = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % words.length);
  };

  const handlePrevious = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev - 1 + words.length) % words.length);
  };

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  if (words.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="body1" color="text.secondary">
          No words to review. Add some words first!
        </Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
      <Typography variant="h6" gutterBottom>
        Card {currentIndex + 1} of {words.length}
      </Typography>
      <Box sx={{ width: '100%', maxWidth: '600px' }}>
        <Flashcard
          word={words[currentIndex]}
          isFlipped={isFlipped}
          onFlip={handleFlip}
        />
      </Box>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="outlined"
          onClick={handlePrevious}
          size="large"
        >
          Previous
        </Button>
        <Button
          variant="outlined"
          onClick={handleNext}
          size="large"
        >
          Next
        </Button>
      </Box>
    </Box>
  );
} 