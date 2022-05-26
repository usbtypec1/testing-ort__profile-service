from sqlalchemy import create_engine
from databases import Database
from sqlalchemy.orm import declarative_base

from core import config

database = Database(config.DATABASE_URL)
engine = create_engine(config.DATABASE_URL)
Base = declarative_base(bind=engine)
