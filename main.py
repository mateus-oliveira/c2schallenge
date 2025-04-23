from fastapi import FastAPI

from app import config, models


app = FastAPI()

models.Base.metadata.create_all(bind=config.engine)

@app.get("/")
async def liveness_probe():
    return {
        'title': 'C2S API',
        'author': 'Mateus Oliveira',
        'date': '23/04/2025',
    }
