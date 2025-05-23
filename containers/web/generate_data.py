from faker import Faker
from sqlalchemy.orm import Session
from app.models import User, Order, Payment, SupportTicket
from app.database import SessionLocal, engine
from datetime import datetime, timedelta, timezone
import random
import uuid

fake = Faker()


def get_current_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_users(db: Session, num: int, recent_days: int = 7):
    users = []
    now = get_current_utc()
    for i in range(num):
        # Ensure some users are created within the last 7 days
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
            id=uuid.uuid4(), name=fake.name(), email=fake.email(), created_at=created_at
        )
        users.append(user)
        db.add(user)
    db.commit()
    return users


def create_orders(db: Session, users: list, num: int):
    orders = []
    now = get_current_utc()
    # Ensure at least one order for a subset of users to be used for failed payments
    failed_payment_user_count = min(5, len(users))
    failed_payment_users = random.sample(users, failed_payment_user_count)
    for user in failed_payment_users:
        order = Order(
            id=uuid.uuid4(),
            user_id=user.id,
            amount=random.uniform(10, 1000),
            status=random.choice(["pending", "completed", "cancelled"]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=30), end_date=now
            ),
        )
        orders.append(order)
        db.add(order)

    # Generate remaining orders
    remaining_orders = num - len(failed_payment_users)
    for i in range(remaining_orders):
        user = random.choice(users)
        created_at = (
            fake.date_time_between(start_date=now - timedelta(days=30), end_date=now)
            if i < remaining_orders // 3  # 33% of orders are recent
            else fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            )
        )
        order = Order(
            id=uuid.uuid4(),
            user_id=user.id,
            amount=random.uniform(10, 1000),
            status=random.choice(["pending", "completed", "cancelled"]),
            created_at=created_at,
        )
        orders.append(order)
        db.add(order)
    db.commit()
    return orders, failed_payment_users


def create_payments(db: Session, orders: list, num: int, failed_payment_users: list):
    payments = []
    now = get_current_utc()
    # Ensure some users have multiple failed payments within the last 60 days
    failed_payment_counts = {
        user.id: random.randint(4, 6) for user in failed_payment_users
    }

    for user_id in failed_payment_counts:
        # Select an order for this user
        user_orders = [o for o in orders if o.user_id == user_id]
        order = random.choice(user_orders)  # Guaranteed to have at least one order
        for _ in range(failed_payment_counts[user_id]):
            payment = Payment(
                id=uuid.uuid4(),
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
            db.add(payment)

    # Generate remaining payments
    remaining_payments = num - sum(failed_payment_counts.values())
    for _ in range(remaining_payments):
        order = random.choice(orders)
        payment = Payment(
            id=uuid.uuid4(),
            order_id=order.id,
            payment_method=random.choice(["credit_card", "paypal", "bank_transfer"]),
            success=random.choice([True, False]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        payments.append(payment)
        db.add(payment)
    db.commit()


def create_support_tickets(db: Session, users: list, num: int):
    tickets = []
    now = get_current_utc()
    # Ensure some users have unresolved tickets
    unresolved_users = random.sample(
        users, min(10, len(users))
    )  # Pick 10 users for unresolved tickets
    for user in unresolved_users:
        ticket = SupportTicket(
            id=uuid.uuid4(),
            user_id=user.id,
            issue=fake.sentence(),
            resolved=False,
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        tickets.append(ticket)
        db.add(ticket)

    # Generate remaining tickets
    remaining_tickets = num - len(unresolved_users)
    for _ in range(remaining_tickets):
        user = random.choice(users)
        ticket = SupportTicket(
            id=uuid.uuid4(),
            user_id=user.id,
            issue=fake.sentence(),
            resolved=random.choice([True, False]),
            created_at=fake.date_time_between(
                start_date=now - timedelta(days=365), end_date=now
            ),
        )
        tickets.append(ticket)
        db.add(ticket)
    db.commit()


def main():
    db = SessionLocal()
    try:
        # 100 users, 25% within last 7 days
        users = create_users(db, 100)

        orders, failed_payment_users = create_orders(db, users, 200)

        # 200 orders, 5 users guaranteed orders
        create_payments(db, orders, 150, failed_payment_users)

        # 150 payments, 5 users with 4-6 failed payments
        create_support_tickets(db, users, 50)

        # 50 tickets, 10 users with unresolved tickets
        print("Data generation complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
