from fastapi import FastAPI
from .routers.auth import authRouter
from .routers.resume import resumeRouter

app=FastAPI()

app.include_router(router=authRouter,tags=["auth"],prefix="/auth")
app.include_router(router=resumeRouter,tags=["resume"],prefix="/resume")

@app.get('/')
def get_root():
    return{"message":"Welcome!"}

