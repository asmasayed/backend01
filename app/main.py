from .core.config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .utils.initDB import create_tables
from .routers.auth import authRouter

#Initialise the db tables when the app starts up
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield


app=FastAPI(lifespan=lifespan)

app.include_router(router=authRouter,tags=["auth"],prefix="/auth")


@app.get('/')
def get_root():
    return{"message":"Welcome!"}

