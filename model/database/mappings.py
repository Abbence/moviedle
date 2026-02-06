from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Float, ARRAY

class Base(DeclarativeBase):
  pass

class TitleAkasRaw(Base):
  __tablename__ = "title_akas_raw"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  ordering: Mapped[int] = mapped_column(Integer, primary_key=True)
  title: Mapped[str] = mapped_column(String, nullable=False)
  region: Mapped[str] = mapped_column(String(4), nullable=True)
  language: Mapped[str] = mapped_column(String(4), nullable=True)
  types: Mapped[str] = mapped_column(String(255), nullable=True)
  attributes: Mapped[str] = mapped_column(String(255), nullable=True)
  isoriginaltitle: Mapped[int] = mapped_column(Integer, nullable=False) # raw data, so it can stay int, will be processed later

class TitleBasicsRaw(Base):
  __tablename__ = "title_basics_raw"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  titletype: Mapped[str] = mapped_column(String(20), nullable=False)
  primarytitle: Mapped[str] = mapped_column(String, nullable=False)
  originaltitle: Mapped[str] = mapped_column(String, nullable=True)
  isadult: Mapped[int] = mapped_column(Integer, nullable=False) # raw data, so it can stay int, will be processed later
  startyear: Mapped[int] = mapped_column(Integer, nullable=True)
  endyear: Mapped[int] = mapped_column(Integer, nullable=True)
  runtimeminutes: Mapped[int] = mapped_column(Integer, nullable=True)
  genres: Mapped[str] = mapped_column(String(255), nullable=True)

class TitleCrewRaw(Base):
  __tablename__ = "title_crew_raw"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  directors: Mapped[str] = mapped_column(String, nullable=True) # actually an array, ',' separated
  writers: Mapped[str] = mapped_column(String, nullable=True) # actually an array, ',' separated

class TitleRatingsRaw(Base):
  __tablename__ = "title_ratings_raw"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  averageRating: Mapped[float] = mapped_column(Float, nullable=True)
  numVotes: Mapped[int] = mapped_column(Integer, nullable=True)

class NameBasicsRaw(Base):
  __tablename__ = "name_basics_raw"
  nameid: Mapped[str] = mapped_column(String(10), primary_key=True)
  primaryname: Mapped[str] = mapped_column(String, nullable=True)
  birthyear: Mapped[int] = mapped_column(Integer, nullable=True)
  deathyear: Mapped[int] = mapped_column(Integer, nullable=True)
  primaryprofession: Mapped[str] = mapped_column(String, nullable=True) # actually an array, ',' separated
  knownfortitles: Mapped[str] = mapped_column(String, nullable=True) # actually an array, ',' separated

class Directors(Base):
  __tablename__ = "directors"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  nameid: Mapped[str] = mapped_column(String(10), primary_key=True)

class Writers(Base):
  __tablename__ = "writers"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  nameid: Mapped[str] = mapped_column(String(10), primary_key=True)

class MoviesFinal(Base):
  __tablename__ = "movies"
  titleid: Mapped[str] = mapped_column(String(10), primary_key=True)
  titletype: Mapped[str] = mapped_column(String(20), nullable=False)
  primarytitle: Mapped[str] = mapped_column(String, nullable=False)
  originaltitle: Mapped[str] = mapped_column(String, nullable=True)
  hungariantitle: Mapped[str] = mapped_column(String, nullable=True)
  isadult: Mapped[bool] = mapped_column(Boolean, nullable=False)
  year: Mapped[int] = mapped_column(Integer, nullable=True)
  runtimeminutes: Mapped[int] = mapped_column(Integer, nullable=True)
  genres: Mapped[set[str]] = mapped_column(ARRAY(String, dimensions=1), nullable=True)
  imdbRating: Mapped[float] = mapped_column(Float, nullable=True)
  imdbVoteCount: Mapped[int] = mapped_column(Integer, nullable=True)
  directorNames: Mapped[set[str]] = mapped_column(ARRAY(String, dimensions=1), nullable=True)

