from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ... import crud, schemas
from ...database import get_db

router = APIRouter()


@router.get(
    "/recent-users", response_model=List[schemas.User], summary="Users from last 7 days"
)
def read_recent_users(days: int = 7, db: Session = Depends(get_db)):
    """Fetch users created in the last N days."""
    return crud.get_recent_users(db, days=days)


@router.get(
    "/orders-by-unresolved-tickets",
    response_model=List[schemas.Order],
    summary="Orders by unresolved tickets",
)
def read_orders_by_unresolved_tickets(db: Session = Depends(get_db)):
    """List orders from users with unresolved support tickets."""
    return crud.get_orders_by_unresolved_ticket_users(db)


@router.get(
    "/total-spent-last-30-days",
    response_model=List[schemas.TotalSpent],
    summary="Total spent last 30 days",
)
def read_total_spent_last_30_days(db: Session = Depends(get_db)):
    """Calculate total spent per user in the last 30 days (successful payments only)."""
    results = crud.get_total_spent_last_30_days(db)
    return [{"user_id": r.id, "total_spent": r.total_spent or 0.0} for r in results]


@router.get(
    "/users-with-failed-payments",
    response_model=List[schemas.User],
    summary="Users with failed payments",
)
def read_users_with_failed_payments(
    days: int = 60, threshold: int = 3, db: Session = Depends(get_db)
):
    """Identify users with more than N failed payments in the last M days."""
    return crud.get_users_with_failed_payments(db, days=days, threshold=threshold)


@router.get(
    "/user-order-stats",
    response_model=List[schemas.UserOrderStats],
    summary="User order statistics",
)
def read_user_order_stats(db: Session = Depends(get_db)):
    """Get first order date, total orders, and support ticket status per user."""
    results = crud.get_user_order_stats(db)
    return [
        {
            "user_id": r.id,
            "first_order_date": r.first_order_date,
            "total_orders": r.total_orders,
            "has_support_ticket": r.has_support_ticket,
        }
        for r in results
    ]
