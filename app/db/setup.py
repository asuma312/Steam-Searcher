import duckdb
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

base_path = os.path.join(
    os.path.dirname(__file__),
    'db_files'
)
os.makedirs(base_path, exist_ok=True)
db_name = "steam-searcher.duckdb"
db_path = os.path.join(base_path, db_name)
DATABASE_URL = f"duckdb:///{db_path}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


