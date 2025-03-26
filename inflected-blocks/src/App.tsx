import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import WordForm from './components/WordForm';
import WordList from './components/WordList';
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
                  <WordForm />
                  <WordList />
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
