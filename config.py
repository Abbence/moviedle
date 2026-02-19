from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL: str = os.environ.get("MOVIEDLE_DATABASE_URL", default='no-db-url-provided')
DATABASE_VERBOSE_LOGGING: bool = os.environ.get("DATABASE_VERBOSE_LOGGING", default="false").lower() == "true"
MOVIEDLE_BLURT_OUT_CANDIDATE_MOVIE: bool = os.environ.get("MOVIEDLE_BLURT_OUT_CANDIDATE_MOVIE", default="false").lower() == "true"
GUESS_THE_MOVIE_BLURT_CANDIDATES: bool = os.environ.get("GUESS_THE_MOVIE_BLURT_CANDIDATES", default="false").lower() == "true"