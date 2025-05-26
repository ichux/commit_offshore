import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@127.0.0.1:16432/{os.getenv('TEST_DB')}"
)

test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_read_users():
    response = client.get("/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_users_negative_limit():
    response = client.get("/v1/users?skip=0&limit=-1")
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be greater than or equal to 0"
    )


def test_read_orders():
    response = client.get("/v1/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_orders_with_user_id():
    response = client.get("/v1/orders?user_id=550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_payments():
    response = client.get("/v1/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_support_tickets():
    response = client.get("/v1/support-tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_recent_users():
    response = client.get("/v1/recent-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_orders_by_unresolved_tickets():
    response = client.get("/v1/orders-by-unresolved-tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_total_spent_last_30_days():
    response = client.get("/v1/total-spent-last-30-days")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_users_with_failed_payments():
    response = client.get("/v1/users-with-failed-payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_user_order_stats():
    response = client.get("/v1/user-order-stats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
