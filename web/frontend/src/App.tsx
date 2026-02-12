import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Game } from './components/Game';
import { HomePage } from './components/HomePage';
import { GuessTheMovieGame } from './components/GuessTheMovieGame';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/moviedle" element={<Game />} />
        <Route path="/guess-the-movie" element={<GuessTheMovieGame />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
