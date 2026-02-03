from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import get_db
from ..models import Tour
from ..schemas import TourOut

router = APIRouter(prefix="/tours", tags=["tours"])


@router.get("", response_model=list[TourOut])
def list_tours(db: Session = Depends(get_db)):
    stmt = select(Tour).where(Tour.is_active.is_(True)).order_by(Tour.tour_id)
    return db.execute(stmt).scalars().all()
