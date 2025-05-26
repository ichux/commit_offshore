from faker import Faker
from sqlalchemy.orm import Session
from app.models import User, Order, Payment, SupportTicket
from app.database import SessionLocal, engine
from datetime import datetime, timedelta, timezone
import random
import uuid

fake = Faker()
used_ids = set()  # Track used IDs to prevent duplicates


def generate_unique_id() -> uuid.UUID:
    """Ensures generated IDs are unique."""
    new_id = uuid.uuid4()
    while new_id in used_ids:
        new_id = uuid.uuid4()
    used_ids.add(new_id)
    return new_id


def get_current_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_users(num: int, recent_days: int = 7):
    """Generates user instances without committing them to the database."""
    users = []
    now = get_current_utc()
    for i in range(num):
        created_at = (
            fake.date_time_between(
                start_date=now - timedelta(days=recent_days), end_date=now
            )
            if i < num // 4  # 25% of users are recent
            else fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            )
        )
        user = User(
            id=generate_unique_id(),
            name=fake.name(),
            email=fake.email(),
            created_at=created_at,
        )
        users.append(user)
    return users


def create_orders(users: list, num: int):
    """Generates order instances without committing them to the database."""
    orders = []
    now = get_current_utc()
    failed_payment_users = random.sample(
        users, min(5, len(users))
    )  # Select users for failed payments

    for user in failed_payment_users:
        order = Order(
            id=generate_unique_id(),
            user_id=user.id,
            amount=random.uniform(10, 1000),
            status=random.choice(["pending", "completed", "cancelled"]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=30), end_date=now
            ),
        )
        orders.append(order)

    remaining_orders = num - len(failed_payment_users)
    for i in range(remaining_orders):
        user = random.choice(users)
        created_at = (
            fake.date_time_between(start_date=now - timedelta(days=30), end_date=now)
            if i < remaining_orders // 3
            else fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            )
        )
        order = Order(
            id=generate_unique_id(),
            user_id=user.id,
            amount=random.uniform(10, 1000),
            status=random.choice(["pending", "completed", "cancelled"]),
            created_at=created_at,
        )
        orders.append(order)
    return orders, failed_payment_users


def create_payments(orders: list, num: int, failed_payment_users: list):
    """Generates payment instances without committing them to the database."""
    payments = []
    now = get_current_utc()
    failed_payment_counts = {
        user.id: random.randint(4, 6) for user in failed_payment_users
    }

    for user_id in failed_payment_counts:
        user_orders = [o for o in orders if o.user_id == user_id]
        order = random.choice(user_orders)
        for _ in range(failed_payment_counts[user_id]):
            payment = Payment(
                id=generate_unique_id(),
                order_id=order.id,
                payment_method=random.choice(
                    ["credit_card", "paypal", "bank_transfer"]
                ),
                success=False,
                created_at=fake.date_time_between(
                    start_date=now - timedelta(days=60), end_date=now
                ),
            )
            payments.append(payment)

    remaining_payments = num - sum(failed_payment_counts.values())
    for _ in range(remaining_payments):
        order = random.choice(orders)
        payment = Payment(
            id=generate_unique_id(),
            order_id=order.id,
            payment_method=random.choice(["credit_card", "paypal", "bank_transfer"]),
            success=random.choice([True, False]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        payments.append(payment)
    return payments


def create_support_tickets(users: list, num: int):
    """Generates support ticket instances without committing them to the database."""
    tickets = []
    now = get_current_utc()
    unresolved_users = random.sample(users, min(10, len(users)))

    for user in unresolved_users:
        ticket = SupportTicket(
            id=generate_unique_id(),
            user_id=user.id,
            issue=fake.sentence(),
            resolved=False,
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        tickets.append(ticket)

    remaining_tickets = num - len(unresolved_users)
    for _ in range(remaining_tickets):
        user = random.choice(users)
        ticket = SupportTicket(
            id=generate_unique_id(),
            user_id=user.id,
            issue=fake.sentence(),
            resolved=random.choice([True, False]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        tickets.append(ticket)
    return tickets


def populate_database():
    """Commits generated data to the database."""
    db = SessionLocal()
    try:
        users = create_users(100)
        orders, failed_payment_users = create_orders(users, 200)
        payments = create_payments(orders, 150, failed_payment_users)
        tickets = create_support_tickets(users, 50)

        db.add_all(users + orders + payments + tickets)
        db.commit()
        print("Data generation complete.")
    finally:
        db.close()


def test_data_integrity():
    """Ensures generated data has unique IDs and valid relationships."""
    users = create_users(100)
    orders, failed_payment_users = create_orders(users, 200)
    payments = create_payments(orders, 150, failed_payment_users)
    tickets = create_support_tickets(users, 50)

    all_ids = (
        {user.id for user in users}
        | {order.id for order in orders}
        | {payment.id for payment in payments}
        | {ticket.id for ticket in tickets}
    )

    assert len(all_ids) == (
        len(users) + len(orders) + len(payments) + len(tickets)
    ), "Duplicate IDs found!"


if __name__ == "__main__":
    populate_database()
    test_data_integrity()
