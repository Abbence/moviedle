from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

from model.database.mappings import Base
import config

from argparse import ArgumentParser

def import_tsv_postgres(session: Session, path: str):
  if not path:
    print("No data file provided for loading, skipping data import.")
    return
  
  print(f"Importing data from '{path}'")

  with open("model/database/import_full_postgres.sql", "r") as f:
    sql_script = f.read().replace("{PATH}", path) # prone to SQL injection
    session.execute(text(sql_script))

  print("Data import complete")

def import_only_final_postgres(session: Session, path: str):
  if not path:
    print("No data file provided for loading, skipping data import.")
    return
  
  if not path.endswith(".tsv"):
    print(f"Provided path '{path}' does not point to a tsv file, skipping data import.")
    return
  
  print(f"Importing only final movies data from '{path}'")

  with open("model/database/import_final_postgres.sql", "r") as f:
    sql_script = f.read().replace("{PATH}", path) # prone to SQL injection
    session.execute(text(sql_script))

  print("Data import complete")

def init_db():
  parser = ArgumentParser()
  parser.add_argument("--schema", action="store_true", help="Create the database schema based on the defined SQLAlchemy models.")
  parser.add_argument("--drop", dest="drop", action="store_true", help="Drop all tables in the database before creating the schema. Use with caution, as this will delete all existing data.")
  parser.add_argument("--only-final", dest="final_tsv_path", type=str, help="Path to tsv file containing only the final movies data, with the same format as the movies table. If provided, it will be loaded instead of the full data.")
  parser.add_argument("--load-data", dest="full_load_dir", type=str, help="Path to tsv file directory for the full data import. The SQL script expects the files to be named in a specific way, see model/database/import_full_postgres.sql for details.")
  args = parser.parse_args()
  
  engine = create_engine(config.DATABASE_URL, echo=config.DATABASE_VERBOSE_LOGGING)

  if args.drop:
    Base.metadata.drop_all(engine)
    print("Dropped all tables")

  if args.schema:
    Base.metadata.create_all(engine)
    print("Created database schema")

  # TODO clean up branches
  if args.final_tsv_path:
    with Session(engine, expire_on_commit=False) as session:

      session.execute(text("SELECT 1"))
      print("Database connection OK")

      #import_only_final_postgres(session, path=args.final_tsv_path)
      session.commit()

      print("Data manipulation...")
      with open("model/database/data_manipulation.sql", "r") as f:
        sql_script = f.read()
        #session.execute(text(sql_script))

      session.commit()
      print("Data manipulation complete")

      print("Adding indexes...")
      with open("model/database/add_trigram_indexes.sql", "r") as f:
        sql_script = f.read()
        session.execute(text(sql_script))

      session.commit()
      print("Indexes added")
    pass
  elif args.full_load_dir:
    print(f"Loading all IMDB data from {args.full_load_dir}...")
    with Session(engine, expire_on_commit=False) as session:

      session.execute(text("SELECT 1"))
      print("Database connection OK")

      import_tsv_postgres(session, path=args.full_load_dir)
      session.commit()

      print("Data manipulation...")
      with open("model/database/data_manipulation.sql", "r") as f:
        sql_script = f.read()
        session.execute(text(sql_script))

      session.commit()
      print("Data manipulation complete")

      print("Adding indexes...")
      with open("model/database/add_trigram_indexes.sql", "r") as f:
        sql_script = f.read()
        session.execute(text(sql_script))

      session.commit()
      print("Indexes added")

  print("Done initializing!")

if __name__ == "__main__":
  init_db()