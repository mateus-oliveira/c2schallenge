from pydantic import BaseModel
from typing import Optional


class Car(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine: Optional[str] = None
    fuel: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    doors: Optional[int] = None
    transmission: Optional[str] = None
    price: Optional[float] = None
    page: Optional[int] = 1
