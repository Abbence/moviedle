from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from web.api.db import get_db_session
from web.api.shared import get_candidator_names, get_movie_by_id
from web.api.moviedle_router import moviedle_router
from web.api.guess_the_movie_router import guess_the_movie_router

from model.game_movie import GameMovie


app = FastAPI(
    title="Moviedle API",
    description="Backend API for Moviedle and Guess the Movie games",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(moviedle_router)
app.include_router(guess_the_movie_router)


@app.get("/")
def read_root():
    return {"status": "ok", "games": ["moviedle", "guess-the-movie"]}


@app.get("/candidators")
def get_candidators() -> list[str]:
    return get_candidator_names()


@app.get("/movie/{title_id}")
def get_movie(title_id: str, db: Session = Depends(get_db_session)) -> GameMovie:
    movie = get_movie_by_id(db, title_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


