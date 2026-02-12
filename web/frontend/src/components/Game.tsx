import React, { useState, useEffect } from 'react';
import { GameMovie, Guess, GameState, GiveUpResponse } from '../types';
import { api } from '../api';
import { SearchBar } from './SearchBar';
import { GuessList } from './GuessList';
import { MovieRow } from './MovieRow';
import styles from './Game.module.css';

/**
 * Main game component orchestrating:
 * - Game initialization and state
 * - Search and guess submission
 * - Game win/lose/give-up states
 */
export const Game: React.FC = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [candidators, setCandidators] = useState<string[]>([]);
  const [selectedCandidator, setSelectedCandidator] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [revealedMovie, setRevealedMovie] = useState<GameMovie | null>(null);

  // Load available candidators on mount
  useEffect(() => {
    const loadCandidators = async () => {
      try {
        const { data } = await api.getCandidators();
        setCandidators(data);
        if (data.length > 0) {
          setSelectedCandidator(data[0]);
        }
      } catch (err) {
        setError('Failed to load candidators');
      }
    };

    loadCandidators();
  }, []);

  // Start a new game
  const handleStartGame = async () => {
    setIsLoading(true);
    setError(null);
    setRevealedMovie(null);

    try {
      const { data } = await api.moviedle.startGame(selectedCandidator);
      setGameState(data);
    } catch (err) {
      setError('Failed to start game');
    } finally {
      setIsLoading(false);
    }
  };

  // Make a guess
  const handleMovieSelected = async (movie: GameMovie) => {
    if (!gameState || gameState.isGameOver) return;

    setIsLoading(true);
    setError(null);

    try {
      const { data: guess } = await api.moviedle.makeGuess(movie.titleid);

      setGameState((prev) => {
        if (!prev) return prev;
        const newState = {
          ...prev,
          guesses: [...prev.guesses, guess],
          tries: prev.tries + 1,
        };

        // Check if game is won
        if (guess.movie.titleid === movie.titleid && Object.values(guess.guess_relations_dict).every(r => r === 'match')) {
          newState.isGameOver = true;
          newState.isGameWon = true;
        }

        return newState;
      });
    } catch (err) {
      setError('Failed to make guess. ' + (err instanceof Error ? err.message : 'Try again.'));
    } finally {
      setIsLoading(false);
    }
  };

  // Give up
  const handleGiveUp = async () => {
    if (!gameState || gameState.isGameOver) return;

    setIsLoading(true);
    setError(null);

    try {
      const { data } = await api.moviedle.giveUp();
      setGameState({
        guesses: data.guesses,
        isGameOver: data.isGameOver,
        isGameWon: data.isGameWon,
        tries: data.tries,
      });
      setRevealedMovie(data.candidateMovie);
    } catch (err) {
      setError('Failed to give up');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.gameContainer}>
      {/* Header */}
      <header className={styles.header}>
        <h1>Moviedle</h1>
        <p>Guess the movie based on its attributes!</p>
      </header>

      {/* Main content */}
      <main className={styles.mainContent}>
        {/* Search section */}
        <section className={styles.searchSection}>
          <SearchBar
            onMovieSelected={handleMovieSelected}
            disabled={!gameState || gameState.isGameOver || isLoading}
          />
        </section>

        {/* Guesses section */}
        {gameState && (
          <section className={styles.guessesSection}>
            <GuessList guesses={gameState.guesses} />
          </section>
        )}
      </main>

      {/* Footer with controls */}
      <footer className={styles.footer}>
        <div className={styles.footerLeft}>
          <select
            value={selectedCandidator}
            onChange={(e) => setSelectedCandidator(e.target.value)}
            disabled={isLoading || (gameState !== null && !gameState.isGameOver)}
            className={styles.candidatorSelect}
          >
            {candidators.map((cand) => (
              <option key={cand} value={cand}>
                {cand}
              </option>
            ))}
          </select>

          <button
            onClick={handleStartGame}
            disabled={isLoading || (gameState !== null && !gameState.isGameOver)}
            className={styles.button}
          >
            {gameState?.isGameOver ? 'New Game' : 'Start Game'}
          </button>
        </div>

        <div className={styles.footerCenter}>
          {gameState && (
            <span className={styles.triesCounter}>
              Tries: {gameState.tries}
            </span>
          )}
        </div>

        <div className={styles.footerRight}>
          <button
            onClick={handleGiveUp}
            disabled={isLoading || !gameState || gameState.isGameOver}
            className={`${styles.button} ${styles.giveUpButton}`}
          >
            Give Up
          </button>
        </div>
      </footer>

      {/* Status messages */}
      {error && (
        <div className={styles.errorBanner}>
          {error}
          <button onClick={() => setError(null)} className={styles.closeButton}>
            ×
          </button>
        </div>
      )}

      {gameState?.isGameWon && (
        <div className={styles.successBanner}>
          🎉 You won! The movie was correctly guessed!
        </div>
      )}

      {gameState?.isGameOver && !gameState.isGameWon && revealedMovie && (
        <div className={styles.modalOverlay} onClick={() => setRevealedMovie(null)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>The movie was:</h2>
              <button
                className={styles.modalCloseButton}
                onClick={() => setRevealedMovie(null)}
              >
                ×
              </button>
            </div>
            <div className={styles.modalContent}>
              <MovieRow movie={revealedMovie} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
