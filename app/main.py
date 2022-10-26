from fastapi import FastAPI

from app.models import models
from app.database.database import engine
from app.routes.route import router


# routes et création des tables


# création des tables
models.Base.metadata.create_all(bind=engine)

# initialisation de FastAPI
app = FastAPI()


app.include_router(router,
                   tags=["Routes"])