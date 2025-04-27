from sqlalchemy.orm import Session

from app.models import schemas, models


def filter_cars(db: Session, filters: schemas.Car):
    """
    Filters cars based on the provided filters.

    Args:
        db (Session): The database session.
        filters (schemas.Car): The filter criteria.

    Returns:
        list: A list of filtered cars.
    """
    query = db.query(models.Car)

    filter_dict = filters.model_dump(exclude_none=True)

    if filter_dict:
        filter_conditions = []
        for key, value in filter_dict.items():
            if key == 'price':
                filter_conditions.append(models.Car.price <= value)
            elif key == 'mileage':
                filter_conditions.append(models.Car.mileage <= value)
            elif key == 'year':
                filter_conditions.append(models.Car.year >= value)
            else:
                filter_conditions.append(getattr(models.Car, key) == value)

        query = query.filter(*filter_conditions)

    return query.all()



