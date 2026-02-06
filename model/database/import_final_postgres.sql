CREATE TEMP TABLE temp_movies (
  titleid TEXT,
  titletype TEXT,
  primarytitle TEXT,
  originaltitle TEXT,
  hungariantitle TEXT,
  year INTEGER,
  runtimeminutes INTEGER,
  genres JSONB,
  isadult BOOLEAN,
  "imdbRating" FLOAT,
  "imdbVoteCount" INTEGER,
  "directorNames" JSONB
);

COPY temp_movies (titleid, titletype, primarytitle, originaltitle, hungariantitle, year, runtimeminutes, genres, isadult, "imdbRating", "imdbVoteCount", "directorNames") from '{PATH}' WITH (FORMAT csv, DELIMITER E'\t', HEADER TRUE, NULL '\N', QUOTE E'"');

INSERT INTO movies (titleid, titletype, primarytitle, originaltitle, hungariantitle, year, runtimeminutes, genres, isadult, "imdbRating", "imdbVoteCount", "directorNames")
SELECT 
  titleid,
  titletype,
  primarytitle,
  originaltitle,
  hungariantitle,
  year,
  runtimeminutes,
  CASE
    WHEN genres IS NULL THEN NULL
    ELSE ARRAY(SELECT jsonb_array_elements_text(genres))
  END,
  isadult,
  "imdbRating",
  "imdbVoteCount",
  CASE
    WHEN "directorNames" IS NULL THEN NULL
    ELSE ARRAY(SELECT jsonb_array_elements_text("directorNames"))
  END
FROM temp_movies;

DROP TABLE temp_movies;

/*
-- Exporting as JSON arrays to properly escape quotes inside arrays. Requires special loading logic (temp table) to convert back to Postgres ARRAYs.
COPY (
  SELECT
    titleid,
    titletype,
    primarytitle,
    originaltitle,
    hungariantitle,
    year,
    runtimeminutes,
    array_to_json(genres) AS genres,
    isadult,
    "imdbRating",
    "imdbVoteCount",
    array_to_json("directorNames") AS directorNames
  FROM movies
)
TO '/tmp/movies.tsv'
WITH (
  FORMAT csv,
  DELIMITER E'\t',
  HEADER true,
  NULL '\N',
  QUOTE '"',
  ESCAPE '"'
);
*/