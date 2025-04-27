import csv

from sqlalchemy import and_, or_

from app.models.models import Base, Car
from app.database.config import SessionLocal, engine

Base.metadata.create_all(bind=engine)


def seed():
    """
    Seed the database with car data from a CSV file.
    This function reads car data from a CSV file, 
    checks for existing records in the database.
    """
    db = SessionLocal()

    with open('app/database/cars.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    total = len(rows)
    new = 0

    filters = [
        (row["brand"], row["model"], row["color"], int(row["year"]))
        for row in rows
    ]

    existing = db.query(Car).filter(
        or_(
            and_(
                Car.brand == brand,
                Car.model == model,
                Car.color == color,
                Car.year == year
            ) for brand, model, color, year in filters
        )
    ).all()

    existing_set = set((car.brand, car.model, car.color, car.year) for car in existing)

    new_cars = []

    for row in rows:
        if (row["brand"], row["model"], row["color"], int(row["year"])) not in existing_set:
            new_car = Car(
                brand=row["brand"],
                model=row["model"],
                year=int(row["year"]),
                engine=row["engine"],
                fuel=row["fuel"],
                color=row["color"],
                mileage=int(row["mileage"]),
                doors=int(row["doors"]),
                transmission=row["transmission"],
                price=float(row["price"])
            )
            new_cars.append(new_car)
            new += 1

    if new_cars:
        db.bulk_save_objects(new_cars)
        db.commit()

    print(f"--- Done ---")
    print(f"Cars in DB: {total}")
    print(f"New created cars: {new}")

    db.close()


if __name__ == "__main__":
    seed()
