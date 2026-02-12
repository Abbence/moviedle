from typing import Optional
from pydantic import BaseModel

from model.game_movie import GameMovie
from model.guess import Guess


class MoviedleGameState(BaseModel):
  candidateMovie: Optional[GameMovie] = None
  guesses: list[Guess] = []
  isGameOver: bool = False
  isGameWon: bool = False
  tries: int = 0