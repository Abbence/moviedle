from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from model.game_movie import GameMovie
from model.guess import Guess
from model.moviedle_game import MoviedleGame
from web.api.db import get_db_session
from web.api.shared import find_movies, get_candidator, get_default_candidator_name, CANDIDATORS
from web.api.moviedle_gamestate import MoviedleGameState


moviedle_router = APIRouter(prefix="/moviedle", tags=["moviedle"])

_current_game: MoviedleGame | None = None


def _get_current_game() -> MoviedleGame:
    if _current_game is None:
        raise HTTPException(status_code=400, detail="Game has not been started yet.")
    return _current_game


@moviedle_router.get("/candidators")
def get_moviedle_candidators() -> list[str]:
    return list(CANDIDATORS.keys())


@moviedle_router.post("/start_game")
def start_game(
    candidator_name: str | None = None,
    db: Session = Depends(get_db_session)
) -> MoviedleGameState:
    global _current_game
    
    if not candidator_name:
        candidator_name = get_default_candidator_name()
    
    candidator = get_candidator(candidator_name)
    if not candidator:
        raise HTTPException(status_code=404, detail=f"No candidator found with name '{candidator_name}'")
    
    _current_game = MoviedleGame(candidator, db)
    
    return MoviedleGameState(
        guesses=_current_game.guesses,
        isGameOver=_current_game.isGameOver,
        isGameWon=_current_game.isGameWon,
        tries=_current_game.get_tries()
    )


@moviedle_router.get("/guesses")
def get_guesses() -> list[Guess]:
    if _current_game is None:
        return []
    return _current_game.guesses


@moviedle_router.post("/make_guess/{titleid}")
def make_guess(titleid: str) -> Guess:
    game = _get_current_game()
    
    try:
        guess = game.make_guess(titleid)
        return guess
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@moviedle_router.post("/give_up")
def give_up() -> MoviedleGameState:
    game = _get_current_game()
    
    game.isGameOver = True
    game.isGameWon = False
    
    return MoviedleGameState(
        candidateMovie=game.candidateMovie,
        guesses=game.guesses,
        isGameOver=game.isGameOver,
        isGameWon=game.isGameWon,
        tries=game.get_tries()
    )


@moviedle_router.get("/find_movies/{title_string}")
def search_movies(
    title_string: str,
    limit: int = 10,
    db: Session = Depends(get_db_session)
) -> list[GameMovie]:
    return find_movies(db, title_string, limit=limit)