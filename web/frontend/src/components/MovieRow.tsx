import React from 'react';
import { GameMovie, Guess, GuessedAttributeRelation, MOVIE_DISPLAY_FIELDS } from '../types';
import { AttributeCell } from './AttributeCell';
import styles from './MovieRow.module.css';

interface MovieRowProps {
  /** For guesses: the guess object; for search results: null */
  guess?: Guess | null;
  /** For search results: the movie object */
  movie?: GameMovie;
  /** Called when search result row is clicked */
  onSelect?: (movie: GameMovie) => void;
  /** Whether this is a clickable search result */
  isSearchResult?: boolean;
}

/**
 * Displays a movie as a row with:
 * - Title information (primarytitle + hungariantitle)
 * - Dynamic attribute cells based on MOVIE_DISPLAY_FIELDS
 * - Color-coded backgrounds for guesses
 * - Fixed column widths matching TableHeader
 * 
 * Extensible: new fields added to MOVIE_DISPLAY_FIELDS automatically appear here
 */
export const MovieRow: React.FC<MovieRowProps> = ({
  guess,
  movie,
  onSelect,
  isSearchResult = false,
}) => {
  const displayMovie = guess?.movie || movie;
  if (!displayMovie) return null;

  const handleClick = () => {
    if (isSearchResult && movie && onSelect) {
      onSelect(movie);
    }
  };

  return (
    <div
      className={`${styles.row} ${isSearchResult ? styles.searchResult : ''}`}
      onClick={handleClick}
      role={isSearchResult ? 'button' : 'listitem'}
      tabIndex={isSearchResult ? 0 : -1}
    >
      {/* Title Column - Fixed Width */}
      <div className={styles.titleColumn}>
        <div className={styles.primaryTitle}>{displayMovie.primarytitle}</div>
        {displayMovie.hungariantitle && (
          <div className={styles.hungarianTitle}>
            ({displayMovie.hungariantitle})
          </div>
        )}
      </div>

      {/* Attribute Cells - Fixed Widths */}
      <div className={styles.attributesContainer}>
        {MOVIE_DISPLAY_FIELDS.map((field) => {
          const value = displayMovie[field as keyof GameMovie];
          const relation = guess?.guess_relations_dict[field] ?? GuessedAttributeRelation.UNKNOWN;

          return (
            <AttributeCell
              key={field}
              value={value}
              relation={relation}
              label={field}
              fieldName={field}
            />
          );
        })}
      </div>
    </div>
  );
};
