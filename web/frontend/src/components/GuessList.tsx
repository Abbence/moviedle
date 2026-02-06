import React from 'react';
import { Guess } from '../types';
import { MovieRow } from './MovieRow';
import { TableHeader } from './TableHeader';
import styles from './GuessList.module.css';

interface GuessesListProps {
  guesses: Guess[];
}

/**
 * Scrollable list of guesses displayed in reverse chronological order
 * (most recent at the top) with a table header.
 */
export const GuessList: React.FC<GuessesListProps> = ({ guesses }) => {
  return (
    <div className={styles.guessesContainer}>
      <div className={styles.guessesHeader}>
        <h2>Guesses ({guesses.length})</h2>
      </div>
      <div className={styles.guessesList}>
        {guesses.length === 0 ? (
          <div className={styles.emptyState}>
            <p>No guesses yet. Start searching for a movie!</p>
          </div>
        ) : (
          <>
            <div className={styles.tableHeaderWrapper}>
              <TableHeader includeTitle={true} />
            </div>
            <div className={styles.guessesContent}>
              {/* Display in reverse order: most recent first */}
              {[...guesses].reverse().map((guess, index) => (
                <div key={guesses.length - index - 1} className={styles.guessItem}>
                  <MovieRow guess={guess} />
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};
