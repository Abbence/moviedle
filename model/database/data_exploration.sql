-- duplicates?
SELECT count(*), primarytitle, originaltitle, hungariantitle --, year, runtimeminutes, count(*), SUM("imdbVoteCount") 
FROM movies 
WHERE primarytitle IS NOT NULL AND originaltitle IS NOT NULL AND hungariantitle IS NOT NULL --AND runtimeminutes IS NOT NULL
GROUP BY primarytitle, originaltitle, hungariantitle --, runtimeminutes
HAVING count(*) > 1 
ORDER BY count(*) DESC;


SELECT * FROM movies;

-- get all "known for" titles for each director of a movie, excluding the original movie itself 
-- probably too complex to be included in the primary table like this, it really needs a separate query if this feature will even be implemented

SELECT
	chosen.titleid,
	array_agg(ROW(
		nbr.primaryname,
		sgd.known_for_titles
		)
	)
FROM 
	(SELECT 'tt0108052' AS titleid) AS chosen
	JOIN directors ON chosen.titleid = directors.titleid 
	JOIN name_basics_raw nbr ON directors.nameid = nbr.nameid 
	LEFT JOIN LATERAL (
		SELECT
			array_agg(DISTINCT tbr_known.primarytitle ) AS known_for_titles
		FROM unnest(string_to_array(nbr.knownfortitles, ',')) AS titlearray(titleid)
			JOIN title_basics_raw tbr_known ON tbr_known.titleid = titlearray.titleid
		WHERE tbr_known.titleid != chosen.titleid
	) sgd ON true
GROUP BY chosen.titleid
;

SELECT * from name_basics_raw nbr WHERE nbr.deathyear is null order by birthyear ;


SELECT 
	LENGTH(nbr.knownfortitles ) - LENGTH(REPLACE(nbr.knownfortitles , ',', '')) + 1 AS known_fors, 
	count(*) 
FROM name_basics_raw nbr 
GROUP BY known_fors 
ORDER BY known_fors desc;



SELECT region, count(*) FROM title_akas_raw GROUP BY region ORDER BY count(*) desc;

SELECT * FROM pg_stat_activity WHERE datname = 'moviedle';

select count(*) from title_basics_raw;


select * from title_basics_raw tbr 
where tbr.primarytitle like '%Son%Saul%';

select * from title_akas_raw tar 
where tar.region = 'HU' and ordering = 2;

SELECT * FROM (SELECT string_to_array(genres, ',') AS genres FROM title_basics_raw tbr) AS converted JOIN (SELECT 'Animation' AS genre) val ON ARRAY[val.genre] <@ converted.genres;



SELECT primarytitle, string_to_array(genres, ',') AS genres FROM title_basics_raw tbr;




SELECT 
	LENGTH(genres) - LENGTH(REPLACE(genres, ',', '')) + 1 AS num_of_genres, 
	count(*) 
FROM title_basics_raw tbr 
WHERE NOT (titletype = 'tvEpisode' OR titletype = 'video' OR titletype = 'videoGame' OR titletype = 'tvPilot')
GROUP BY num_of_genres;

SELECT * FROM title_basics_raw tbr WHERE tbr.primarytitle ILIKE '%Son of Saul%';

SELECT titletype, isadult, count(*) FROM title_basics_raw tbr GROUP BY titletype, isadult;

SELECT * FROM title_basics_raw tbr WHERE titletype = 'tvSeries';

SELECT titletype, count(*) FROM movies GROUP BY titletype;

SELECT primarytitle, count(*) from title_basics_raw WHERE titletype = 'tvSeries' group by primarytitle order by count(*) desc;

SELECT * FROM title_basics_raw tbr WHERE primarytitle ilike 'House'; OR tbr.primarytitle ilike '%Doctor%House%';


SELECT * FROM title_basics_raw WHERE NOT (titletype = 'tvEpisode' OR titletype = 'video' OR titletype = 'videoGame' OR titletype = 'tvPilot') AND titletype is null;


SELECT * FROM movies WHERE titletype = 'tvMiniSeries' ORDER BY "imdbVoteCount" DESC NULLS LAST;
