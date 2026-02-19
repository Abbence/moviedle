from typing import Optional
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session
import config
from model.candidation_types import ICandidationType, NotNullAttributeCandidator
from model.database.mappings import MoviesFinal
from model.game_movie import GameMovie, TitleType

class MovieAttributes(BaseModel):
  titleType: TitleType
  year: int
  runtimeMinutes: int
  imdbRating: float
  imdbVoteCount: int
  directorNames: set[str]
  genres: set[str]

  @staticmethod
  def from_gamemovie(game_movie: GameMovie) -> "MovieAttributes":
    if game_movie.titleType is None or game_movie.year is None or game_movie.runtimeMinutes is None or game_movie.imdbRating is None or game_movie.imdbVoteCount is None or game_movie.directorNames is None or game_movie.genres is None:
      raise ValueError("GameMovie has null attributes, cannot convert to MovieAttributes")
    
    return MovieAttributes(
      titleType=game_movie.titleType,
      year=game_movie.year,
      runtimeMinutes=game_movie.runtimeMinutes,
      imdbRating=game_movie.imdbRating,
      imdbVoteCount=game_movie.imdbVoteCount,
      directorNames=game_movie.directorNames,
      genres=game_movie.genres
    )

"""
Manages multiple secret movies and their attributes. The player has to guess the title for each set of attributes.
"""
class GuessTheMoviesGame():
  def __init__(self, db_session: Session, candidation_type: ICandidationType, slot_count: int): 
    self.candidator = candidation_type
    self.slotCount = slot_count
    self.session = db_session

    self.guessed_mask: list[bool] = [False] * self.slotCount
    self._secret_films : list[GameMovie] = self._candidate_random_movies()

    if config.GUESS_THE_MOVIE_BLURT_CANDIDATES:
      print("Generated candidate movies:")
      for idx, movie in enumerate(self._secret_films):
        print(f"Slot {idx}: {movie.primarytitle} ({movie.titleid})")
        print(f"IMDB link: https://www.imdb.com/title/{movie.titleid}/")

  def _candidate_random_movies(self) -> list[GameMovie]:
    # NOTE: Primitive random selection method on database level, not efficient for large candidate sets.
    query_stmt = select(MoviesFinal)\
      .where(self.candidator.get_candidation_filter(), NotNullAttributeCandidator().get_candidation_filter())\
      .order_by(func.random())\
      .limit(self.slotCount)
    
    result = self.session.execute(query_stmt).scalars().all()

    if not result:
      raise Exception("Candidates could not be found with the given candidation filter and session")
    
    if len(result) < self.slotCount:
      print("WARN: less candidates than slots:", len(result), "<", self.slotCount)
      self.slotCount = len(result)
      self.guessed_mask = [False] * self.slotCount

    return [GameMovie.from_moviesfinal(movie) for movie in result]
  
  def get_attributes(self) -> list[MovieAttributes]:
    return [MovieAttributes.from_gamemovie(movie) for movie in self._secret_films]
  
  def get_score(self) -> int:
    return sum(self.guessed_mask)
  
  def make_guess(self, guess_slot: int, guessed_titleid: str) -> bool:
    if guess_slot < 0 or guess_slot >= self.slotCount:
      raise ValueError(f"Invalid guess slot: {guess_slot}. Must be between 0 and {self.slotCount - 1}.")
    
    if self.guessed_mask[guess_slot]:
      raise ValueError(f"Slot {guess_slot} has already been guessed.")
    
    # NOTE: the existence of the parameter guessed_titleid is not even checked in the database. 
    # This could potentially be misleading if the frontend messes up the titleid-s somehow because the user will never know that their guess was not even valid.

    if guessed_titleid == self._secret_films[guess_slot].titleid: 
      print(f"Correct guess for slot {guess_slot}: {self._secret_films[guess_slot].primarytitle}")
      self.guessed_mask[guess_slot] = True


    return self.guessed_mask[guess_slot]