from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session

from model.database.mappings import MoviesFinal
from model.game_movie import GameMovie
from model.candidation_types import ICandidationType, Pop500K_HasHungarianTitleCandidator, TopNVoteCountCandidator


CANDIDATORS: dict[str, ICandidationType] = {
    "pop500": Pop500K_HasHungarianTitleCandidator(),
    "top10": TopNVoteCountCandidator(10),
    "top30": TopNVoteCountCandidator(30),
}

def get_candidator_names() -> list[str]:
    return list(CANDIDATORS.keys())

def get_candidator(name: str) -> ICandidationType | None:
    return CANDIDATORS.get(name)

def get_default_candidator_name() -> str:
    return next(iter(CANDIDATORS.keys()))


def find_movies(db: Session, title_search_text: str, limit: int = 10) -> list[GameMovie]:
    search_term = f"%{title_search_text.lower()}%"
    
    stmt = select(MoviesFinal).where(
        or_(
            MoviesFinal.primarytitle.ilike(search_term),
            MoviesFinal.originaltitle.ilike(search_term),
            MoviesFinal.hungariantitle.ilike(search_term)
        )
    ).order_by(
        MoviesFinal.imdbVoteCount.desc().nulls_last()
    ).limit(limit)
    
    results = db.execute(stmt).scalars().all()
    return [GameMovie.from_moviesfinal(movie) for movie in results]


def get_movie_by_id(db: Session, title_id: str) -> GameMovie | None:
    stmt = select(MoviesFinal).where(MoviesFinal.titleid == title_id).limit(1)
    result = db.execute(stmt).scalar_one_or_none()
    
    if result:
        return GameMovie.from_moviesfinal(result)
    return None
