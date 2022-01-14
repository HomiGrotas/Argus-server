import pytest


from app import create_app, db

app = create_app()
db.drop_all(app=app)
db.create_all(app=app)


@pytest.fixture
def client():
    """A test client for the app."""
    return app.test_client()
