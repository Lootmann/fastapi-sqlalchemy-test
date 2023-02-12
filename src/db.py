from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///dev.db"

engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)


def get_db():
    with session() as s:
        yield s
