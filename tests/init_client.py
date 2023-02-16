import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db import get_db
from src.main import app
from src.models.user import Base

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_client() -> TestClient:
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    TestSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def override_get_db():
        try:
            db = TestSession()
            Base.metadata.create_all(bind=engine)
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app=app, base_url="http://test") as client:
        yield client
