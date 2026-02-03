from datetime import date, datetime
from pydantic import BaseModel, Field


class TourOut(BaseModel):
    tour_id: int
    tour_name: str
    country: str
    city: str | None
    nights: int
    base_price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=200)
    phone: str = Field(min_length=3, max_length=30)
    tour_id: int
    persons: int = Field(ge=1, le=20)
    start_date: date


class OrderOut(BaseModel):
    order_id: int
    full_name: str
    phone: str
    tour_id: int
    persons: int
    start_date: date
    created_at: datetime

    class Config:
        from_attributes = True
