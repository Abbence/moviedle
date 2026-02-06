import React from 'react';
import { MOVIE_DISPLAY_FIELDS } from '../types';
import styles from './TableHeader.module.css';

interface TableHeaderProps {
  includeTitle?: boolean;
}

/**
 * Table header row matching MovieRow column widths.
 * Automatically reads from MOVIE_DISPLAY_FIELDS - just add fields there to extend.
 */
export const TableHeader: React.FC<TableHeaderProps> = ({ includeTitle = true }) => {
  const getFieldLabel = (field: string): string => {
    // Convert camelCase to Title Case with spaces
    // e.g., "imdbRating" -> "Imdb Rating", "directorNames" -> "Director Names"
    return field
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, (str) => str.toUpperCase())
      .trim();
  };

  return (
    <div className={styles.headerRow}>
      {includeTitle && (
        <div className={styles.titleHeader}>
          <span>Title</span>
        </div>
      )}
      <div className={styles.attributesHeader}>
        {MOVIE_DISPLAY_FIELDS.map((field) => (
          <div key={field} className={styles.columnHeader} data-field={field}>
            {getFieldLabel(field)}
          </div>
        ))}
      </div>
    </div>
  );
};
