import React, { useState, useCallback, useRef, useEffect } from 'react';
import { GameMovie } from '../types';
import { api } from '../api';
import { MovieRow } from './MovieRow';
import styles from './SearchBar.module.css';

interface SearchBarProps {
  onMovieSelected: (movie: GameMovie) => void;
  disabled?: boolean;
}

/**
 * Interactive search bar with debounced search API calls.
 * Displays movie suggestions in a dropdown that closes when a movie is selected.
 */
export const SearchBar: React.FC<SearchBarProps> = ({ onMovieSelected, disabled = false }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<GameMovie[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const debounceRef = useRef<NodeJS.Timeout>();
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Debounced search
  const performSearch = useCallback(async (searchTerm: string) => {
    if (!searchTerm.trim()) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const { data } = await api.moviedle.findMovies(searchTerm);
      setResults(data);
      setIsOpen(true);
    } catch (err) {
      setError('Failed to search movies');
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleInputChange = (value: string) => {
    setQuery(value);

    // Clear existing timeout
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Debounce search
    debounceRef.current = setTimeout(() => {
      performSearch(value);
    }, 300);
  };

  const handleMovieSelect = (movie: GameMovie) => {
    onMovieSelected(movie);
    setQuery('');
    setResults([]);
    setIsOpen(false);
  };

  // Close dropdown when clicking outside
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
    <div ref={containerRef} className={styles.searchBarContainer}>
      <div className={styles.searchInputWrapper}>
        <input
          ref={inputRef}
          type="text"
          placeholder="Search for a movie..."
          value={query}
          onChange={(e) => handleInputChange(e.target.value)}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          disabled={disabled}
          className={styles.searchInput}
        />
        {isLoading && <div className={styles.spinner} />}
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {isOpen && results.length > 0 && (
        <div className={styles.dropdown}>
          {results.map((movie) => (
            <div key={movie.titleid} className={styles.dropdownItem}>
              <MovieRow movie={movie} isSearchResult onSelect={handleMovieSelect} />
            </div>
          ))}
        </div>
      )}

      {isOpen && query.trim() && results.length === 0 && !isLoading && (
        <div className={styles.noResults}>No movies found</div>
      )}
    </div>
  );
};
