from pydantic import BaseModel
from typing import Optional
from random import Random
import enum

from sqlalchemy.sql.expression import ColumnElement, text
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, create_engine

import config
from model.candidation_types import ICandidationType, NotNullAttributeCandidator, Pop500K_HasHungarianTitleCandidator, TopNVoteCountCandidator
from model.database.mappings import MoviesFinal
from model.guess import Guess

from model.game_movie import GameMovie

"""
Candidate constraint: cannot have any of its values null - that would greatly increase difficulty (in guessing too, but also it would require telling the contestants these null values in advance since it will not match with any of their matches)
"""
class MoviedleGame:
  def __init__(self, candidator: ICandidationType, db_session: Session):
    self.db_session: Session = db_session
    self.candidator: ICandidationType = candidator

    self.guesses: list[Guess] = []
    self.isGameOver: bool = False
    self.isGameWon: bool = False

    self.candidateMovie = self._generate_random_candidate(candidator)

    if config.MOVIEDLE_BLURT_OUT_CANDIDATE_MOVIE:
      print(f"Generated candidate movie: {self.candidateMovie}")
      print(f"IMDB link: https://www.imdb.com/title/{self.candidateMovie.titleid}/")

  def get_tries(self) -> int:
    return len(self.guesses)

  def _generate_random_candidate(self, candidator: ICandidationType) -> GameMovie:
    """
    Generates random film candidate using given candidator.
    Fetches many films and disregards all but one randomly selected film.
    """

    # NOTE: Primitive random selection method on database level, not efficient for large candidate sets.
    query_stmt = select(MoviesFinal)\
      .where(candidator.get_candidation_filter(), NotNullAttributeCandidator().get_candidation_filter())\
      .order_by(func.random())\
      .limit(1)

    result = self.db_session.execute(query_stmt).scalar_one_or_none()

    if not result:
      raise Exception("No candidate movies found with the given candidation filter.")
    
    return GameMovie.from_moviesfinal(result)
    
  def make_guess(self, guessed_movie_titleid: str) -> Guess:
    if self.isGameOver:
      raise Exception("Game is already over. No more guesses allowed.")

    guess_stmt = select(MoviesFinal).where(MoviesFinal.titleid == guessed_movie_titleid)
    guessed_movie_orm: Optional[MoviesFinal] = self.db_session.execute(guess_stmt).scalar_one_or_none()

    if not guessed_movie_orm:
      raise ValueError(f"Guessed movie with titleid '{guessed_movie_titleid}' not found in database.")

    guessed_movie: GameMovie = GameMovie.from_moviesfinal(guessed_movie_orm)
    guess: Guess = Guess.create(guessed_movie, candidate_movie=self.candidateMovie)

    self.guesses.append(guess)

    # Check for game over
    if guess.is_perfect_guess():
      self.isGameOver = True
      self.isGameWon = True

    return guess
  
