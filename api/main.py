from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app import ai, daos
from app.config.cors import cors
from app.database import config
from app.models import models, schemas


app = FastAPI()
app.add_middleware(**cors)
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


@app.get("/cars/ai")
async def get_cars_with_ai(
    sentence: Annotated[str, Query()],
    db: Session = Depends(config.get_db)
):
    """
    Filter cars using AI interpretation of the input sentence.
    """
    parameters = ai.llm_interpreter(sentence)
    return daos.filter_cars(db, schemas.Car(**parameters))
