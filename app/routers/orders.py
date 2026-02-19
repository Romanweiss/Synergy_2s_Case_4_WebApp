from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Order, Service, Tour
from ..schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    stmt = select(Order).order_by(Order.order_id.desc())
    return db.execute(stmt).scalars().all()


@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    tour = db.get(Tour, payload.tour_id)
    if not tour or not tour.is_active:
        raise HTTPException(status_code=404, detail="Tour not found or inactive")

    if payload.service_id is not None:
        service = db.get(Service, payload.service_id)
        if not service or not service.is_active:
            raise HTTPException(status_code=404, detail="Service not found or inactive")

    order = Order(
        full_name=payload.full_name,
        phone=payload.phone,
        tour_id=payload.tour_id,
        service_id=payload.service_id,
        persons=payload.persons,
        start_date=payload.start_date,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
