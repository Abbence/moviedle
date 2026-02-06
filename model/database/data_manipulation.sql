INSERT INTO directors (titleid, nameid)
SELECT
    a.titleid,
	e.director
FROM title_crew_raw a
CROSS JOIN LATERAL unnest(string_to_array(a.directors, ',')) AS e(director);

INSERT INTO writers (titleid, nameid)
SELECT
    a.titleid,
	e.writer
FROM title_crew_raw a
CROSS JOIN LATERAL unnest(string_to_array(a.directors, ',')) AS e(writer);


INSERT INTO movies (titleid, titletype, primarytitle, originaltitle, hungariantitle, year, runtimeminutes, genres, isadult, "imdbRating", "imdbVoteCount", "directorNames")
SELECT 
	tbr.titleid,
	tbr.titletype,
	tbr.primarytitle,
	tbr.originaltitle,
	MAX(ta_HU.title) AS title_hu,
	tbr.startyear AS year,
	tbr.runtimeminutes,
	string_to_array(genres, ',') AS genres,
	tbr.isadult = 1, 
	MAX(trr."averageRating") AS imdbRating,
	MAX(trr."numVotes") AS imdbVoteCount,
	array_agg(nbr.primaryname) AS director_names
FROM title_basics_raw tbr 
	LEFT JOIN title_akas_raw ta_HU ON tbr.titleid = ta_HU.titleid
	LEFT JOIN title_ratings_raw trr ON tbr.titleid = trr.titleid
	LEFT JOIN 
		(directors dir 
			JOIN name_basics_raw nbr ON dir.nameid = nbr.nameid
		) ON tbr.titleid = dir.titleid 
WHERE 1=1
	AND (ta_HU.region = 'HU' OR ta_HU.region IS NULL)
	AND ARRAY[tbr.titletype]::text[] <@ ARRAY['movie', 'short', 'tvMiniSeries', 'tvMovie', 'tvSeries', 'tvShort', 'tvSpecial']
	-- AND (tbr.titletype = 'movie' OR tbr.titletype = 'short' OR tbr.titletype = 'tvMiniSeries' OR tbr.titletype = 'tvMovie' OR tbr.titletype = 'tvSeries' OR tbr.titletype = 'tvShort' OR tbr.titletype = 'tvSpecial')
GROUP BY tbr.titleid
;

UPDATE movies SET "directorNames" = NULL WHERE "directorNames"::text[] = ARRAY[NULL];
