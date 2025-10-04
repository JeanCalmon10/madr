import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db, Base
from app.main import app

#  Set up a database for testing
SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}, # Required for SQLite to work with multiple threads in the FastAPI environment
    poolclass=StaticPool,
)

# Create SessionLocal for testing that binds to the testing engine
Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The scope='function' means a new database session is created for each test function
@pytest.fixture(scope='function', name='session')
def session_fixture():
    """
    Create a new isolated database session.
    """

    # Create all tabeles in-memory database
    Base.metadata.create_all(bind=engine)

    # Create a database session to be used
    db = Testing_SessionLocal()

    try:
        # Yield provides the session to the test function
        yield db
    finally:
        # CLEANUP (TEARDOWN): Run after the test
        db.close()

        # Delete all tables (guarantees that the database stays clean)
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name='client')
# The 'client' fixture depends on the 'session' fixture
def client_fixture(session):
    """
    Create the TestClient and manage the dependency override.
    """

    # Dependency override function that will provide the testing session
    def override_get_db():
        # Returns the object yielded by the session fixture
        try:
            yield session
        finally:
            # Guarantee the session is closed after use although in this case it is managed by the session fixture
            session.close()

    # Tell FastAPI to use the override function for the get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create a TestClient that will be used in the tests
    client = TestClient(app)

    # The 'yield' statement provides the client to the test function
    yield client

    # Reset the dependency overrides after the test function completes
    app.dependency_overrides.clear()


