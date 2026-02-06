import enum
from typing import Optional
from pydantic import BaseModel

from model.database.mappings import MoviesFinal

class TitleType(enum.Enum):
  MOVIE = "movie"
  SHORT = "short"
  SERIES = "series"

  @staticmethod
  def from_imdbtype(label: str) -> "TitleType | None":
    if label in ["movie", "tvMovie", "tvSpecial"]:
      return TitleType.MOVIE
    elif label in ["short", "tvShort"]:
      return TitleType.SHORT
    elif label in ["tvSeries", "tvMiniSeries"]:
      return TitleType.SERIES
    
    return None

class GameMovie(BaseModel):
  titleid: str
  primarytitle: str
  titleType: Optional[TitleType]
  year: Optional[int]
  originaltitle: Optional[str]
  hungariantitle: Optional[str]
  runtimeMinutes: Optional[int]
  imdbRating: Optional[float]
  imdbVoteCount: Optional[int]
  directorNames: Optional[set[str]]
  genres: Optional[set[str]]

  @staticmethod
  def from_moviesfinal(movie_orm: MoviesFinal) -> "GameMovie":
    return GameMovie(
      titleid=movie_orm.titleid,
      primarytitle=movie_orm.primarytitle,
      originaltitle=movie_orm.originaltitle,
      hungariantitle=movie_orm.hungariantitle,
      titleType=TitleType.from_imdbtype(movie_orm.titletype),
      year=movie_orm.year,
      runtimeMinutes=movie_orm.runtimeminutes,
      imdbRating=movie_orm.imdbRating,
      imdbVoteCount=movie_orm.imdbVoteCount,
      directorNames=movie_orm.directorNames,
      genres=movie_orm.genres
    )