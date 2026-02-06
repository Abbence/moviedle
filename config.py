from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL: str = os.environ.get("MOVIEDLE_DATABASE_URL", default='no-db-url-provided')
DATABASE_VERBOSE_LOGGING: bool = os.environ.get("DATABASE_VERBOSE_LOGGING", default="false").lower() == "true"