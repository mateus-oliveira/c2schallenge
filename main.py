from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from typing import Annotated


from app import daos
from app.models import models, schemas
from app.database import config


app = FastAPI()

models.Base.metadata.create_all(bind=config.engine)

@app.get("/")
async def liveness_probe():
    return {
        'title': 'C2S API',
        'author': 'Mateus Oliveira',
        'date': '23/04/2025',
    }

@app.get("/cars")
async def get_cars(
    filters: Annotated[schemas.Car, Query()],
    db: Session = Depends(config.get_db),
):
    """
    Filter cars from the database.
    """
    return daos.filter_cars(db, filters)