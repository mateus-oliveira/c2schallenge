import pytest

from app.models import schemas, models
from app.daos import filter_cars

from tests.helpers import db

CARS = [
    models.Car(id=1, brand="TOYOTA", model="COROLLA", year=2020, price=25000, mileage=30000),
    models.Car(id=2, brand="HONDA", model="CIVIC", year=2019, price=22000, mileage=40000),
    models.Car(id=3, brand="BMW", model="X5", year=2021, price=50000, mileage=20000),
]


@pytest.mark.parametrize(
    "filters, expected",
    [
        (schemas.Car(brand="TOYOTA"), 1),
        (schemas.Car(model="CIVIC"), 1),
        (schemas.Car(year=2020), 2),
        (schemas.Car(price=25000), 2),
        (schemas.Car(mileage=30000), 2),
        (schemas.Car(doors=4), 0),
        (schemas.Car(transmission="AUTOMATIC"), 0),
    ],
)
def test_filter_cars(db, filters, expected):
    """ Test the filter_cars function with various filters. """
    db.bulk_save_objects(CARS)
    result = filter_cars(db, filters)
    assert len(result) == expected
