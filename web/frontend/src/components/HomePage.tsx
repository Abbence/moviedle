import React from 'react';
import { Link } from 'react-router-dom';
import styles from './HomePage.module.css';

export const HomePage: React.FC = () => (
  <div className={styles.homeContainer}>
    <h1>Welcome to Moviedle!</h1>
    <div className={styles.linksContainer}>
      <Link to="/moviedle" className={styles.gameLink}>Play Moviedle</Link>
      <Link to="/guess-the-movie" className={styles.gameLink}>Play Guess the Movie</Link>
    </div>
  </div>
);
