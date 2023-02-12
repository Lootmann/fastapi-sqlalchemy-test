import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.user import Base
from src.db import get_db
from src.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture
def test_client():
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False},
    )

    TestSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestSession()
            yield db
        finally:
            db.close()
            Base.metadata.drop_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, base_url="http://test") as client:
        yield client
