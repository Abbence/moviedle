import React, { useState, useCallback, useRef, useEffect } from 'react';
import { GameMovie, MovieAttributes, MOVIE_DISPLAY_FIELDS } from '../types';
import { api } from '../api';
import { AttributeCell } from './AttributeCell';
import { GuessedAttributeRelation } from '../types';
import styles from './SlotRow.module.css';

interface SlotRowProps {
  slot: number;
  attributes: MovieAttributes;
  isGuessed: boolean;
  guessedTitle?: string;
  onGuess: (slot: number, movie: GameMovie) => void;
}

export const SlotRow: React.FC<SlotRowProps> = ({
  slot,
  attributes,
  isGuessed,
  guessedTitle,
  onGuess,
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<GameMovie[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();
  const containerRef = useRef<HTMLDivElement>(null);

  const performSearch = useCallback(async (searchTerm: string) => {
    if (!searchTerm.trim()) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    setIsLoading(true);
    try {
      const { data } = await api.gtm.findMovies(searchTerm);
      setResults(data);
      setIsOpen(true);
    } catch {
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleInputChange = (value: string) => {
    setQuery(value);

    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(() => {
      performSearch(value);
    }, 300);
  };

  const handleMovieSelect = (movie: GameMovie) => {
    onGuess(slot, movie);
    setQuery('');
    setResults([]);
    setIsOpen(false);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (!containerRef.current) return;
      const targetNode = event.target as Node;
      if (!containerRef.current.contains(targetNode)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`${styles.slotRow} ${isGuessed ? styles.guessed : ''}`}>
      {/* Title/Search Column */}
      <div className={styles.titleColumn} ref={containerRef}>
        {isGuessed ? (
          <div className={styles.guessedTitle}>
            <span className={styles.checkmark}>✓</span>
            {guessedTitle}
          </div>
        ) : (
          <div className={styles.searchWrapper}>
            <input
              type="text"
              placeholder="Search movie title..."
              value={query}
              onChange={(e) => handleInputChange(e.target.value)}
              onFocus={() => results.length > 0 && setIsOpen(true)}
              className={styles.searchInput}
            />
            {isLoading && <div className={styles.spinner} />}

            {isOpen && results.length > 0 && (
              <div className={styles.dropdown}>
                {results.map((movie) => (
                  <div
                    key={movie.titleid}
                    className={styles.dropdownItem}
                    onClick={() => handleMovieSelect(movie)}
                  >
                    <div className={styles.movieTitle}>{movie.primarytitle}</div>
                    {movie.hungariantitle && (
                      <div className={styles.movieSubtitle}>({movie.hungariantitle})</div>
                    )}
                    {movie.year && <span className={styles.movieYear}>{movie.year}</span>}
                  </div>
                ))}
              </div>
            )}

            {isOpen && query.trim() && results.length === 0 && !isLoading && (
              <div className={styles.noResults}>No movies found</div>
            )}
          </div>
        )}
      </div>

      {/* Attribute Cells */}
      <div className={styles.attributesContainer}>
        {MOVIE_DISPLAY_FIELDS.map((field) => {
          const value = attributes[field as keyof MovieAttributes];
          const displayValue = Array.isArray(value) ? value : value;

          return (
            <AttributeCell
              key={field}
              value={displayValue as string | number | string[]}
              relation={GuessedAttributeRelation.UNKNOWN}
              label={field}
              fieldName={field}
            />
          );
        })}
      </div>
    </div>
  );
};
