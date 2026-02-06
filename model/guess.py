import enum

from pydantic import BaseModel

from model.game_movie import GameMovie


class GuessedAttributeRelation(enum.Enum):
  """
  Relation of guessed attribute to the actual candidate's attribute.
  Higher means the candidate's attribute is higher than the guessed one (e.g. year: candidate 2000, guessed 1990 -> HIGHER)
  Partial should be used for set-like attributes (e.g. director names, genres) when there is a partial but not full match.
  Unknown is used when the guess's attribute relation is null.
  """
  HIGHER = "higher"
  LOWER = "lower"
  MATCH = "match"
  NO_MATCH = "no-match"
  PARTIAL = "partial"
  UNKNOWN = "unknown"

class Guess(BaseModel):
  movie: GameMovie
  guess_relations_dict: dict[str, GuessedAttributeRelation]

  @staticmethod
  def create(movie: GameMovie, candidate_movie: GameMovie | None = None) -> "Guess":
    """
    Create a guess object cotaining the guessed movie.
    If no candidate_movie is provided, all attribute relations are set to UNKNOWN.
    If candidate_movie is provided, also evaluate the guess's relations based on the candidate movie.
    """
    guess = Guess(
      movie=movie,
      guess_relations_dict={key: GuessedAttributeRelation.UNKNOWN for key in movie.model_dump().keys()}
    )

    if candidate_movie:
      guess.evaluate_guess(candidate_movie)

    return guess
  
  def is_perfect_guess(self) -> bool:
    return all(relation == GuessedAttributeRelation.MATCH for relation in self.guess_relations_dict.values())
  
  def evaluate_guess(self, candidate: GameMovie):
    """
    Set guess's relations to appropriate values based on self.movie and the `candidate` argument
    """
    for attribute_name, candidate_value in candidate.model_dump().items():
      guessed_value = self.movie.model_dump().get(attribute_name)

      # Null-value attributes
      if guessed_value is None:
        self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.UNKNOWN
        continue

      # Numeric attributes
      if attribute_name in ["year", "runtimeMinutes", "imdbRating", "imdbVoteCount"]:
        if candidate_value < guessed_value:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.LOWER
        elif candidate_value > guessed_value:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.HIGHER
        else:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.MATCH

      # Set-like attributes
      elif attribute_name in ["directorNames", "genres"]:
        if guessed_value == candidate_value:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.MATCH
        elif guessed_value & candidate_value:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.PARTIAL
        else:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.NO_MATCH

      # Default attribute comparison
      else:
        if guessed_value == candidate_value:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.MATCH
        else:
          self.guess_relations_dict[attribute_name] = GuessedAttributeRelation.NO_MATCH

    return self
