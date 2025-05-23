from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple, Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models


def get_current_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[type[models.User]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_orders(
    db: Session, user_id: Optional[UUID] = None, skip: int = 0, limit: int = 100
) -> list[type[models.Order]]:
    query = db.query(models.Order)
    if user_id:
        query = query.filter(models.Order.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_payments(
    db: Session, skip: int = 0, limit: int = 100
) -> list[type[models.Payment]]:
    return db.query(models.Payment).offset(skip).limit(limit).all()


def get_support_tickets(
    db: Session, skip: int = 0, limit: int = 100
) -> list[type[models.SupportTicket]]:
    return db.query(models.SupportTicket).offset(skip).limit(limit).all()


def get_recent_users(db: Session, days: int = 7) -> list[type[models.User]]:
    now = get_current_utc()
    date_threshold = now - timedelta(days=days)
    return db.query(models.User).filter(models.User.created_at >= date_threshold).all()


def get_orders_by_unresolved_ticket_users(db: Session) -> list[type[models.Order]]:
    subquery = (
        db.query(models.SupportTicket.user_id)
        .filter(models.SupportTicket.resolved == False)
        .distinct()
    )
    return db.query(models.Order).filter(models.Order.user_id.in_(subquery)).all()


def get_users_with_failed_payments(
    db: Session, days: int = 60, threshold: int = 3
) -> list[type[models.User]]:
    now = get_current_utc()
    date_threshold = now - timedelta(days=days)
    subquery = (
        db.query(models.User.id, func.count(models.Payment.id).label("failed_payments"))
        .join(models.Order, models.User.id == models.Order.user_id)
        .join(models.Payment, models.Order.id == models.Payment.order_id)
        .filter(
            models.Payment.success == False, models.Payment.created_at >= date_threshold
        )
        .group_by(models.User.id)
        .having(func.count(models.Payment.id) > threshold)
        .subquery()
    )
    return db.query(models.User).join(subquery, models.User.id == subquery.c.id).all()


def get_user_order_stats(
    db: Session,
) -> List[Tuple[UUID, Optional[datetime], int, bool]]:
    return (
        db.query(
            models.User.id,
            func.min(models.Order.created_at).label("first_order_date"),
            func.count(models.Order.id).label("total_orders"),
            func.bool_or(models.SupportTicket.id.isnot(None)).label(
                "has_support_ticket"
            ),
        )
        .outerjoin(models.Order)
        .outerjoin(models.SupportTicket)
        .group_by(models.User.id)
        .all()
    )


def get_total_spent_last_30_days(db: Session) -> List[Tuple[UUID, float]]:
    now = get_current_utc()
    date_threshold = now - timedelta(days=30)
    return (
        db.query(models.User.id, func.sum(models.Order.amount).label("total_spent"))
        .join(models.Order)
        .join(models.Payment)
        .filter(
            models.Payment.success == True, models.Payment.created_at >= date_threshold
        )
        .group_by(models.User.id)
        .all()
    )
