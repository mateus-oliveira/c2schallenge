from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    engine = Column(String)
    fuel = Column(String)
    color = Column(String)
    mileage = Column(Integer)
    doors = Column(Integer)
    transmition = Column(String)
    price = Column(Float)
