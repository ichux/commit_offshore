from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ... import crud, schemas
from ...database import get_db
from typing import List, Optional
from uuid import UUID

router = APIRouter()


@router.get("/users", response_model=List[schemas.User], summary="List all users")
def read_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=0, le=1000, description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of users."""
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/orders", response_model=List[schemas.Order], summary="List orders")
def read_orders(
    user_id: Optional[UUID] = None,
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        100,
        ge=0,
        le=1000,
        description="Maximum number of records to return",
    ),
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of orders, optionally filtered by user_id."""
    return crud.get_orders(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/payments", response_model=List[schemas.Payment], summary="List payments")
def read_payments(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        100,
        ge=0,
        le=1000,
        description="Maximum number of records to return",
    ),
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of payments."""
    return crud.get_payments(db, skip=skip, limit=limit)


@router.get(
    "/support-tickets",
    response_model=List[schemas.SupportTicket],
    summary="List support tickets",
)
def read_support_tickets(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        100,
        ge=0,
        le=1000,
        description="Maximum number of records to return",
    ),
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of support tickets."""
    tickets = crud.get_support_tickets(db, skip=skip, limit=limit)
    return tickets
