"""
Test configuration — SQLite in-memory database + TestClient fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.main import app
from app.models.usuario import RolUsuario, Usuario

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Provide a database session for tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """TestClient for unauthenticated requests."""
    return TestClient(app)


@pytest.fixture
def director_user(db: Session) -> Usuario:
    """Create and return a director user."""
    user = Usuario(
        email="director@test.co",
        nombre_completo="Director Test",
        hashed_password=get_password_hash("Test1234"),
        rol=RolUsuario.DIRECTOR,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def tecnico_user(db: Session) -> Usuario:
    """Create and return a residente técnico user."""
    user = Usuario(
        email="tecnico@test.co",
        nombre_completo="Técnico Test",
        hashed_password=get_password_hash("Test1234"),
        rol=RolUsuario.RESIDENTE_TECNICO,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_token(client: TestClient, email: str, password: str = "Test1234") -> str:
    """Helper to get JWT token for a user."""
    res = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture
def director_token(client: TestClient, director_user: Usuario) -> str:
    """JWT token for director user."""
    return get_token(client, director_user.email)


@pytest.fixture
def tecnico_token(client: TestClient, tecnico_user: Usuario) -> str:
    """JWT token for técnico user."""
    return get_token(client, tecnico_user.email)


def auth_header(token: str) -> dict:
    """Build Authorization header."""
    return {"Authorization": f"Bearer {token}"}
