import React from 'react';
import { GuessedAttributeRelation } from '../types';
import styles from './AttributeCell.module.css';

interface AttributeCellProps {
  value: string | number | string[] | undefined | null;
  relation: GuessedAttributeRelation;
  label?: string;
  fieldName?: string;
}

/**
 * Displays a single attribute cell with color-coded background based on guess relation.
 * Shows an indicator arrow/symbol based on the relation type.
 * For set fields (genres, directorNames), displays items vertically with truncation.
 */
export const AttributeCell: React.FC<AttributeCellProps> = ({
  value,
  relation,
  label,
  fieldName,
}) => {
  const getIndicator = () => {
    switch (relation) {
      case GuessedAttributeRelation.HIGHER:
        return '↑';
      case GuessedAttributeRelation.LOWER:
        return '↓';
      case GuessedAttributeRelation.MATCH:
        return '✓';
      case GuessedAttributeRelation.NO_MATCH:
        return '✗';
      case GuessedAttributeRelation.PARTIAL:
        return '◐';
      case GuessedAttributeRelation.UNKNOWN:
        return null;
    }
  };

  const isSetField = fieldName === 'genres' || fieldName === 'directorNames';
  const MAX_VISIBLE_ITEMS = 3;
  const indicator = getIndicator();

  const renderContent = () => {
    if (!value) return '—';

    if (Array.isArray(value)) {
      const items = value;
      const visibleItems = items.slice(0, MAX_VISIBLE_ITEMS);
      const hasMore = items.length > MAX_VISIBLE_ITEMS;
      const fullList = items.join('\n');

      return (
        <div className={styles.setContent} title={fullList}>
          {visibleItems.map((item, idx) => (
            <div key={idx} className={styles.setItem}>
              {item}
            </div>
          ))}
          {hasMore && (
            <div className={styles.moreIndicator}>
              +{items.length - MAX_VISIBLE_ITEMS} more
            </div>
          )}
        </div>
      );
    }

    return String(value);
  };

  return (
    <div
      className={`${styles.cell} ${styles[relation]} ${isSetField ? styles.setCell : ''}`}
      title={label}
      data-field={fieldName}
    >
      {indicator && <div className={styles.indicator}>{indicator}</div>}
      <div className={styles.content}>
        {renderContent()}
      </div>
    </div>
  );
};
