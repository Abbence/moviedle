from sqlalchemy import ColumnElement, and_, select, inspect
from sqlalchemy.orm import Mapper

from model.database.mappings import MoviesFinal


class ICandidationType:
  def get_candidation_filter(self) -> ColumnElement[bool]:
    return ColumnElement()
  
class CherryPickedCandidator_1(ICandidationType):
  def get_candidation_filter(self) -> ColumnElement[bool]:
    return MoviesFinal.primarytitle.ilike("Son of Saul")
  
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