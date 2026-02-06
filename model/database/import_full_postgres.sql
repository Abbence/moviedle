-- Importing

-- IMDB has double quotes (") dangling inside title fields, so quoting should be "turned off"
copy title_basics_raw from '{PATH}/title.basics.tsv' WITH (format csv, DELIMITER E'\t', header true, null '\N', quote E'\b');

copy title_akas_raw from '{PATH}/title.akas.hu.tsv' WITH (format csv, DELIMITER E'\t', header true, null '\N', quote E'\b');

copy title_crew_raw from '{PATH}/title.crew.tsv' WITH (format csv, DELIMITER E'\t', header true, null '\N', quote E'\b');

copy title_ratings_raw from '{PATH}/title.ratings.tsv' WITH (format csv, DELIMITER E'\t', header true, null '\N', quote E'\b');

copy name_basics_raw from '{PATH}/name.basics.tsv' WITH (format csv, DELIMITER E'\t', header true, null '\N', quote E'\b');

-- check copy progress
select cast(bytes_processed as float)/bytes_total as progress, * from pg_stat_progress_copy;