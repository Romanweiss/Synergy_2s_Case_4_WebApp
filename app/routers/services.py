from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Service
from ..schemas import ServiceOut

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    stmt = select(Service).where(Service.is_active.is_(True)).order_by(Service.service_id)
    return db.execute(stmt).scalars().all()
