/* Type definitions matching backend */

export interface GameMovie {
  titleid: string;
  primarytitle: string;
  year?: number;
  originaltitle?: string;
  hungariantitle?: string;
  runtimeMinutes?: number;
  imdbRating?: number;
  imdbVoteCount?: number;
  directorNames?: string[];
  genres?: string[];
}

export enum GuessedAttributeRelation {
  HIGHER = 'higher',
  LOWER = 'lower',
  MATCH = 'match',
  NO_MATCH = 'no-match',
  PARTIAL = 'partial',
  UNKNOWN = 'unknown',
}

export interface Guess {
  movie: GameMovie;
  guess_relations_dict: Record<string, GuessedAttributeRelation>;
}

export interface GameState {
  guesses: Guess[];
  isGameOver: boolean;
  isGameWon: boolean;
  tries: number;
}

export interface GiveUpResponse {
  guesses: Guess[];
  isGameOver: boolean;
  isGameWon: boolean;
  tries: number;
  revealedCandidateMovie: GameMovie;
}

/* Configuration */
export const API_BASE_URL = '/api';
export const SEARCH_DEBOUNCE_MS = 300;

/**
 * Fields to display in MovieRow and table header.
 * 
 * TO ADD A NEW COLUMN:
 * 1. Add the field name here
 * 2. Define column width in AttributeCell.module.css and TableHeader.module.css
 *    (search for "Fixed widths" comment and add your field)
 * 3. If it's a set-like field (array), add to isSetField check in AttributeCell.tsx
 * 4. Optionally add comparison logic in backend's Guess.evaluate_guess() if needed
 */
export const MOVIE_DISPLAY_FIELDS = [
  'titleType',
  'year',
  'runtimeMinutes',
  'imdbRating',
  'imdbVoteCount',
  'directorNames',
  'genres',
] as const;
