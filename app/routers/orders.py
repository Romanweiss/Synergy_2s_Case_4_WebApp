from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Order, Tour
from ..schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    # Проверим, что тур существует и активен
    tour = db.get(Tour, payload.tour_id)
    if not tour or not tour.is_active:
        # FastAPI сам превратит это в 422/400? Лучше 404:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Tour not found or inactive")

    order = Order(
        full_name=payload.full_name,
        phone=payload.phone,
        tour_id=payload.tour_id,
        persons=payload.persons,
        start_date=payload.start_date,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
