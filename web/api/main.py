from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from model.database.mappings import MoviesFinal

from sqlalchemy import create_engine, select, or_, func
from sqlalchemy.orm import Session

from config import DATABASE_URL, DATABASE_VERBOSE_LOGGING
from model.game_movie import GameMovie
from model.guess import Guess
from model.moviedle_game import MoviedleGame
from model.candidation_types import ICandidationType, Pop500K_HasHungarianTitleCandidator, TopNVoteCountCandidator

app = FastAPI()

game: MoviedleGame | None = None

candidators: dict[str, ICandidationType]= {
  "pop500": Pop500K_HasHungarianTitleCandidator(),
  "top10": TopNVoteCountCandidator(10),
  "top30": TopNVoteCountCandidator(30)
}

db_engine = create_engine(DATABASE_URL, echo=DATABASE_VERBOSE_LOGGING)

game_session = Session(db_engine)
# TODO session.close()

class GameState(BaseModel):
  candidateMovie: Optional[GameMovie] = None
  guesses: list[Guess] = []
  isGameOver: bool = False
  isGameWon: bool = False
  tries: int = 0

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/candidators")
def get_candidators() -> list[str]:
  return list(candidators.keys())

@app.post("/start_game")
def start_game(candidator_name: str | None = None) -> GameState:
  global game
  
  if not candidator_name:
    candidator_name = next(iter(candidators.keys())) # use first candidator as default

  if candidator_name not in candidators.keys():
    raise HTTPException(status_code=404, detail=f"No candidator found with name {candidator_name}")

  candidator = candidators[candidator_name]
  game = MoviedleGame(candidator, game_session)
  
  return GameState(
    guesses=game.guesses,
    isGameOver=game.isGameOver,
    isGameWon=game.isGameWon,
    tries=game.get_tries()
  )


@app.get("/guesses")
def get_guesses() -> list[Guess]:
  if not game:
    return []
  
  return game.guesses

@app.post("/make_guess/{titleid}")
def make_guess(titleid: str) -> Guess:
  if not game:
    raise HTTPException(status_code=400, detail="Game has not been started yet.")
  
  try:
    guess = game.make_guess(titleid)
    return guess
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

@app.post("/give_up")
def give_up() -> GameState:
  if not game:
    raise HTTPException(status_code=400, detail="Game has not been started yet.")
  
  game.isGameOver = True
  game.isGameWon = False
  
  return GameState(
    candidateMovie=game.candidateMovie,
    guesses=game.guesses,
    isGameOver=game.isGameOver,
    isGameWon=game.isGameWon,
    tries=game.get_tries()
  )
  
@app.get("/find_movies/{titleString}")
def find_movies(titleString: str, limit: int = 10) -> list[GameMovie]:
  """
  Search for movies by partial title match across primary, original, and Hungarian titles.
  Uses PostgreSQL trigram similarity for fast substring matching.
  Results are ordered by relevance (similarity score) and popularity (vote count).
  """
  search_term = f"%{titleString.lower()}%"
  with Session(db_engine) as session:  
    # Use trigram similarity for fuzzy matching (requires pg_trgm extension and GIN indexes)
    stmt = select(MoviesFinal).where(
      or_(
        func.lower(MoviesFinal.primarytitle).like(search_term),
        func.lower(MoviesFinal.originaltitle).like(search_term),
        func.lower(MoviesFinal.hungariantitle).like(search_term)
      )
    ).order_by(
      # Order by popularity (most voted movies first, NULLs last)
      MoviesFinal.imdbVoteCount.desc().nulls_last()
    ).limit(limit)
    
    results = session.execute(stmt).scalars().all()
    
    return [GameMovie.from_moviesfinal(movie) for movie in results]

@app.get("/movie/{titleId}")
def get_movie_by_titleid(titleId: str) -> GameMovie:
  with Session(db_engine) as session:
    stmt = select(MoviesFinal)\
    .where(
      MoviesFinal.titleid == titleId
    ).limit(1)

    result = session.execute(stmt).scalar_one_or_none()

    if not result:
      raise HTTPException(status_code=404, detail="Movie not found")
    
    return GameMovie.from_moviesfinal(result)


