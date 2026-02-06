# Moviedle (filmkóba)

Attribútum alapú **kitalálós játék filmekkel** - kiadás éve, műfajok, időtartam, IMDB értékelés, rendezők, stb. viszonya alapján lehet találgatni a rejtélyes filmre. 


## Technológiák
Kliens-szerver modellel működő webalkalmazás, **React** frontenddel és **FastAPI** backenddel, illetve az **IMDB adatbázisa** alapján épített saját, lokális adatbázissal. Jelenleg a projekt **PostgreSQL**-t használ, de csak a CSV importálás és a fuzzy text search (trigram) indexek specifikusak erre az SQL dialektusra.

## Adatbázis előkészítése ("felhasználói")

Le kell tölteni egy kész adatbázis-exportot: [Drive link, 2026.02.06.](https://drive.google.com/file/d/1BfZ5TUf2meVDVxIXv16I5SJ0jGWwvHv_/view)

Szükséges létrehozni egy PostgreSQL adatbázist a szerverünkön. Például:
```sql
psql -u username

CREATE DATABASE moviedle;
GRANT ALL PRIVILEGES ON DATABASE moviedle TO username;

GRANT pg_read_server_files TO username;

ALTER ROLE username WITH SUPERUSER; -- az indexek bekapcsolása miatt kell csak, tulajdonképpen kihagyható lépés

-- PostgreSQL 15-től szükségesek lehetnek a következők is:
\c moviedle
GRANT ALL PRIVILEGES ON SCHEMA public TO username;
```

### Python környezet és init_db.py

```bash
# javasolt virtual environment használata, például: python -m venv .venv && source ./venv/bin/activate
pip install -r requirements.txt
```

Állítsuk be az adatbázis elérési URL-jét a `MOVIEDLE_DATABASE_URL` környezeti változóban, vagy a `.env` fájlban (lásd: `.env.example`)
Például:
```bash
MOVIEDLE_DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
```

Az `init_db.py` script egybefoglalja az adatbázisséma létrehozását, az adatok importálását és végül az indexek létrehozását. 

Felhasználói célra csak a végleges adathalmaz betöltéséhez futtassuk a következőt (ez eltarthat akár pár percig is):

```bash
python init_db.py --schema --only-final /path/movies.tsv
```

**FONTOS** *: az elérési útvonal az **adatbázisszerveren** értendő. Lokális gép esetén is a **'postgres'** felhasználónak el kell tudnia érni a fájlokat (illetve az összes mappát a fájlig!), **teljes jogosultságokkal** kell rendelkeznie felettük.*

*Ezen kívül az **adatbázis-felhasználónak** valószínűleg rendelkeznie kell legalább a `pg_read_server_files` jogosultsággal (lásd: [PostgreSQL dokumentáció](https://www.postgresql.org/docs/current/predefined-roles.html#PREDEFINED-ROLE-PG-READ-SERVER-FILES))*

## Adatbázis előkészítése (fejlesztői)

Az alkalmazás által használható adatbázis kialakításahoz az IMDB adataiból kell kiindulni, ezeket kell a (PostgreSQL) adatbázisszerverre feltölteni, az adatbázisba importálni. Ez után már az adatbáziskezelő-rendszer eszközeivel szűrjük ki és kapcsoljuk össze a játék számára fontos adatokat egy külön táblába - ezzel fogunk végül dolgozni.

Szükséges létrehozni egy PostgreSQL adatbázist a szerverünkön. Például:
```sql
psql -u username

CREATE DATABASE moviedle;
GRANT ALL PRIVILEGES ON DATABASE moviedle TO username;

GRANT pg_read_server_files TO username;

ALTER ROLE username WITH SUPERUSER; -- az indexek bekapcsolása miatt kell csak, tulajdonképpen kihagyható lépés

-- PostgreSQL 15-től szükségesek lehetnek a következők is:
\c moviedle
GRANT ALL PRIVILEGES ON SCHEMA public TO username;
```

### Adatok beszerzése
Az [IMDB oldaláról](https://datasets.imdbws.com/) be kell szerezni az alábbi TSV fájlokat: 
- name.basics.tsv.gz
- title.akas.tsv.gz
- title.basics.tsv.gz
- title.crew.tsv.gz 
- title.ratings.tsv.gz

(Ezek kicsomagolva összesen max 5-10 GB helyet foglalnak)

### Python környezet és init_db.py

```bash
# javasolt virtual environment használata, például: python -m venv .venv && source ./venv/bin/activate
pip install -r requirements.txt
```

Állítsuk be az adatbázis elérési URL-jét a `MOVIEDLE_DATABASE_URL` környezeti változóban, vagy a `.env` fájlban (lásd: `.env.example`)
Például:
```bash
MOVIEDLE_DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
```

Az `init_db.py` script egybefoglalja az adatbázisséma létrehozását, az IMDB adatok importálását, az adatmanipulációt és végül az indexek létrehozását. 

Fejlesztői célra az IMDB adatok megtartásával együtt futtassuk a következőt (ez eltarthat akár 10-15 percig is!):
```bash
python init_db.py --schema --load-data /path/to/csvs/
```

**FONTOS** *: az elérési útvonal az **adatbázisszerveren** értendő. Lokális gép esetén is a **'postgres'** felhasználónak el kell tudnia érni a fájlokat (illetve az összes mappát a fájlig!), **teljes jogosultságokkal** kell rendelkeznie felettük.*

*Ezen kívül az **adatbázis-felhasználónak** valószínűleg rendelkeznie kell legalább a `pg_read_server_files` jogosultsággal (lásd: [PostgreSQL dokumentáció](https://www.postgresql.org/docs/current/predefined-roles.html#PREDEFINED-ROLE-PG-READ-SERVER-FILES))*

### [Opcionális] Gyorsabb adatfeldolgozás szövegesen
Mivel a legnagyobb állomány a `title.akas.tsv` és ennek csak azokat a sorait használjuk, amiben magyar címek vannak (ez a fájl méretéhez képest elég kevés) - megspórolhatjuk az adatbázisszerverre való feltöltésüket egy egyszerű szöveges előfeldolgozással.

```bash
head -n 1 title.akas.tsv > title.akas.hu.tsv
cat title.akas.tsv | egrep $'([[:alnum:][:punct:] -:_]*\t){3}HU' >> title.akas.hu.tsv
```

Ezután viszont szükséges az `import_full_postgres.sql` fájlban a `title.akas.tsv` fájlnevet átírni az új fájlnévre.

## Webalkalmazás futtatása

### Backend futtatása

```bash
uvicorn web.api.main:app
```

### Frontend futtatása

Fejlesztésre:
```bash
cd web/frontend
nvm use 24
npm install
npm run dev
```

Build:
```bash
cd web/frontend
nvm use 24
npm install
npm run build
# ezután a web/frontend/dist mappában megtalálhatóak a szükséges fájlok
```
