from sqlalchemy import ColumnElement, and_, select, inspect
from sqlalchemy.orm import Mapper

from model.database.mappings import MoviesFinal


class ICandidationType:
  def get_candidation_filter(self) -> ColumnElement[bool]:
    return ColumnElement()
  
class CherryPickedCandidator(ICandidationType):
  def __init__(self, titleids: str | list[str]):
    self.title_list: list[str] = titleids if isinstance(titleids, list) else [titleids]

  def get_candidation_filter(self) -> ColumnElement[bool]:
    return MoviesFinal.titleid.in_(self.title_list)

class HasGenreCandidator(ICandidationType):
  def __init__(self, genres: str | list[str]):
    self.genres: set[str] = set(genres)

  def get_candidation_filter(self) -> ColumnElement[bool]:
    return MoviesFinal.genres.contains(self.genres)
  
class Pop500K_HasHungarianTitleCandidator(ICandidationType):
  def get_candidation_filter(self) -> ColumnElement[bool]:
    return and_(MoviesFinal.imdbVoteCount >= 500000, MoviesFinal.hungariantitle != None)
  
class TopNVoteCountCandidator(ICandidationType):
  def __init__(self, topN: int = 50):
    if topN <= 0:
      raise ValueError("topN must be a positive integer.")
    self.topN = topN

  def get_candidation_filter(self) -> ColumnElement[bool]:
    return MoviesFinal.titleid.in_(
      select(MoviesFinal.titleid).where(MoviesFinal.imdbVoteCount != None).order_by(MoviesFinal.imdbVoteCount.desc()).limit(self.topN)
    )

class NotNullAttributeCandidator(ICandidationType):
  def get_candidation_filter(self) -> ColumnElement[bool]:
    mapper: Mapper[MoviesFinal] = inspect(MoviesFinal)
    conditions = [col != None for col in mapper.columns if col.nullable]
    return and_(*conditions)