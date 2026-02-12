from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from model.guess_the_movie import GuessTheMoviesGame, MovieAttributes
from web.api.db import get_db_session
from web.api.shared import get_candidator, get_default_candidator_name, CANDIDATORS


guess_the_movie_router = APIRouter(prefix="/guess_the_movie", tags=["guess_the_movie"])


class GuessTheMovieState(BaseModel):
    slot_count: int
    guessed_mask: list[bool]
    score: int
    attributes: list[MovieAttributes]


class GuessResult(BaseModel):
    correct: bool
    slot: int
    score: int


_current_game: GuessTheMoviesGame | None = None


def _get_current_game() -> GuessTheMoviesGame:
    if _current_game is None:
        raise HTTPException(status_code=400, detail="Game has not been started yet.")
    return _current_game


@guess_the_movie_router.get("/candidators")
def get_gtm_candidators() -> list[str]:
    return list(CANDIDATORS.keys())


@guess_the_movie_router.post("/start_game")
def start_game(
    slot_count: int = 5,
    candidator_name: str | None = None,
    db: Session = Depends(get_db_session)
) -> GuessTheMovieState:
    global _current_game
    
    if not candidator_name:
        candidator_name = get_default_candidator_name()
    
    candidator = get_candidator(candidator_name)
    if not candidator:
        raise HTTPException(status_code=404, detail=f"No candidator found with name '{candidator_name}'")
    
    _current_game = GuessTheMoviesGame(db, candidator, slot_count)
    
    return GuessTheMovieState(
        slot_count=_current_game.slotCount,
        guessed_mask=_current_game.guessed_mask,
        score=_current_game.get_score(),
        attributes=_current_game.get_attributes()
    )


@guess_the_movie_router.get("/state")
def get_game_state() -> GuessTheMovieState:
    game = _get_current_game()
    
    return GuessTheMovieState(
        slot_count=game.slotCount,
        guessed_mask=game.guessed_mask,
        score=game.get_score(),
        attributes=game.get_attributes()
    )


@guess_the_movie_router.post("/guess/{slot}/{titleid}")
def make_guess(slot: int, titleid: str) -> GuessResult:
    game = _get_current_game()
    
    try:
        correct = game.make_guess(slot, titleid)
        return GuessResult(correct=correct, slot=slot, score=game.get_score())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@guess_the_movie_router.get("/score")
def get_score() -> int:
    game = _get_current_game()
    return game.get_score()
