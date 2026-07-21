from fastapi import FastAPI
from .routers.auth import authRouter
from .routers.resume import router


app=FastAPI()

app.include_router(router=authRouter,tags=["auth"],prefix="/auth")
app.include_router(router=router)

@app.get('/')
def get_root():
    return{"message":"Welcome!"}

