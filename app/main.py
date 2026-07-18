from fastapi import FastAPI
from .routers.auth import authRouter

app=FastAPI()

app.include_router(router=authRouter,tags=["auth"],prefix="/auth")

@app.get('/')
def get_root():
    return{"message":"Welcome!"}

