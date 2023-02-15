from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///dev.db"

engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    with session() as s:
        yield s
