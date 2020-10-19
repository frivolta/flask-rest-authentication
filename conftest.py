import pytest

from auth import create_app
from auth.extensions import db


@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()
