from pydantic import BaseModel
from typing import Optional
from random import Random
import enum

from sqlalchemy.sql.expression import ColumnElement, text
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, create_engine

from model.candidation_types import ICandidationType, NotNullAttributeCandidator, Pop500K_HasHungarianTitleCandidator, TopNVoteCountCandidator
from model.database.mappings import MoviesFinal
from model.guess import Guess

from model.game_movie import GameMovie

notNullCandidator: ICandidationType = NotNullAttributeCandidator()

"""
Candidate constraint: cannot have any of its values null - that would greatly increase difficulty (in guessing too, but also it would require telling the contestants these null values in advance since it will not match with any of their matches)

TODO dependency: Table?
"""
class MoviedleGame:
  def __init__(self, candidator: ICandidationType, db_session: Session):
    self.db_session: Session = db_session
    self.candidator: ICandidationType = candidator

    self.guesses: list[Guess] = []
    self.isGameOver: bool = False
    self.isGameWon: bool = False

    self.candidateMovie = self.generate_random_candidate(candidator)

    print(f"Generated candidate movie: {self.candidateMovie}") # TODO remove or log properly

  def get_tries(self) -> int:
    return len(self.guesses)

  def generate_random_candidate(self, candidator: ICandidationType) -> GameMovie:
    """
    Generates random film candidate using given candidator.
    Fetches many films and disregards all but one randomly selected film.
    """

    # Random generation done in Python. NOTE Upgrade idea: do it completely inside database
    rand_val: float = Random().random()

    count_stmt = select(func.count(MoviesFinal.titleid)).where(candidator.get_candidation_filter(), notNullCandidator.get_candidation_filter())
    query_stmt = select(MoviesFinal).where(candidator.get_candidation_filter(), notNullCandidator.get_candidation_filter())

    size: int = self.db_session.execute(count_stmt).scalar_one_or_none() or 0
    candidate_index = int(size * rand_val) + 1

    result = self.db_session.execute(query_stmt.limit(candidate_index)).scalars().all()

    if not result:
      raise Exception("No candidate movies found with the given candidation filter.")
    
    candidate: MoviesFinal = result[-1]

    return GameMovie.from_moviesfinal(candidate)
    
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
  
