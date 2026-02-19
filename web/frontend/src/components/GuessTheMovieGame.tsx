import React, { useState, useEffect } from 'react';
import { GameMovie, GTMGameState } from '../types';
import { api } from '../api';
import { SlotRow } from './SlotRow';
import { TableHeader } from './TableHeader';
import styles from './GuessTheMovieGame.module.css';

interface GuessedMovie {
  primarytitle: string;
  hungariantitle?: string;
}

export const GuessTheMovieGame: React.FC = () => {
  const [gameState, setGameState] = useState<GTMGameState | null>(null);
  const [guessedMovies, setGuessedMovies] = useState<(GuessedMovie | null)[]>([]);
  const [candidators, setCandidators] = useState<string[]>([]);
  const [selectedCandidator, setSelectedCandidator] = useState<string>('');
  const [slotCount, setSlotCount] = useState<number>(5);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ slot: number; correct: boolean } | null>(null);

  useEffect(() => {
    loadCandidators();
  }, []);

  const loadCandidators = async () => {
    try {
      const { data } = await api.gtm.getCandidators();
      setCandidators(data);
      if (data.length > 0) {
        setSelectedCandidator(data[0]);
      }
    } catch {
      setError('Failed to load candidators');
    }
  };

  const startNewGame = async () => {
    setIsLoading(true);
    setError(null);
    setFeedback(null);

    try {
      const { data } = await api.gtm.startGame(slotCount, selectedCandidator || undefined);
      setGameState(data);
      setGuessedMovies(new Array(data.slot_count).fill(null));
    } catch (err) {
      setError('Failed to start game. ' + (err instanceof Error ? err.message : ''));
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuess = async (slot: number, movie: GameMovie) => {
    if (!gameState || gameState.guessed_mask[slot]) return;

    setFeedback(null);

    try {
      const { data } = await api.gtm.makeGuess(slot, movie.titleid);

      if (data.correct) {
        setGameState((prev) => {
          if (!prev) return prev;
          const newMask = [...prev.guessed_mask];
          newMask[slot] = true;
          return { ...prev, guessed_mask: newMask, score: data.score };
        });
        setGuessedMovies((prev) => {
          const newMovies = [...prev];
          newMovies[slot] = {
            primarytitle: movie.primarytitle,
            hungariantitle: movie.hungariantitle,
          };
          return newMovies;
        });
        setFeedback({ slot, correct: true });
      } else {
        setFeedback({ slot, correct: false });
      }

      setTimeout(() => setFeedback(null), 2000);
    } catch (err) {
      setError('Failed to make guess. ' + (err instanceof Error ? err.message : ''));
    }
  };

  const isGameComplete = gameState?.guessed_mask.every((g) => g);

  return (
    <div className={styles.gameContainer}>
      <header className={styles.header}>
        <h1>Guess the Movie</h1>
        <p>Identify the movies from their attributes!</p>
      </header>

      <main className={styles.mainContent}>
        {!gameState ? (
          <div className={styles.setupPanel}>
            <h2>Start a New Game</h2>
            <div className={styles.setupOptions}>
              <label className={styles.optionLabel}>
                Number of Movies:
                <select
                  value={slotCount}
                  onChange={(e) => setSlotCount(Number(e.target.value))}
                  className={styles.select}
                >
                  {[3, 5, 7, 10].map((n) => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </label>
              <label className={styles.optionLabel}>
                Candidator:
                <select
                  value={selectedCandidator}
                  onChange={(e) => setSelectedCandidator(e.target.value)}
                  className={styles.select}
                  disabled={candidators.length === 0}
                >
                  {candidators.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </label>
            </div>
            <button
              onClick={startNewGame}
              disabled={isLoading}
              className={styles.startButton}
            >
              {isLoading ? 'Starting...' : 'Start Game'}
            </button>
          </div>
        ) : (
          <div className={styles.gameArea}>
            <TableHeader />
            <div className={styles.slotsList}>
              {gameState.attributes.map((attr, index) => (
                <SlotRow
                  key={index}
                  slot={index}
                  attributes={attr}
                  isGuessed={gameState.guessed_mask[index]}
                  guessedMovie={guessedMovies[index] ?? undefined}
                  onGuess={handleGuess}
                />
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerLeft}>
          <select
            value={selectedCandidator}
            onChange={(e) => setSelectedCandidator(e.target.value)}
            className={styles.candidatorSelect}
            disabled={candidators.length === 0 || !gameState}
          >
            {candidators.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
        <div className={styles.footerCenter}>
          {gameState && (
            <span className={styles.scoreCounter}>
              Score: {gameState.score} / {gameState.slot_count}
            </span>
          )}
        </div>
        <div className={styles.footerRight}>
          <button
            onClick={startNewGame}
            disabled={isLoading}
            className={styles.button}
          >
            New Game
          </button>
        </div>
      </footer>

      {error && (
        <div className={styles.errorBanner}>
          {error}
          <button onClick={() => setError(null)} className={styles.closeButton}>
            ×
          </button>
        </div>
      )}

      {feedback && (
        <div className={feedback.correct ? styles.successBanner : styles.wrongBanner}>
          {feedback.correct
            ? `✓ Correct! Movie ${feedback.slot + 1} guessed!`
            : `✗ Wrong guess for movie ${feedback.slot + 1}. Try again!`}
        </div>
      )}

      {isGameComplete && (
        <div className={styles.completeBanner}>
          🎉 Congratulations! You identified all movies!
        </div>
      )}
    </div>
  );
};
