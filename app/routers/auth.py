from ..database.schemas.user import UserResponse,UserCreate,UserToken,UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..core.db import get_db
from ..services.userService import UserService

authRouter=APIRouter()

@authRouter.post("/signup",status_code=201,response_model=UserResponse)
def signUp(
    signUpDetails:UserCreate,
    session:Session=Depends(get_db)
):
    try:
        return UserService(session=session).signup(user_details=signUpDetails)
    except Exception as e:
        print(e)
        raise e
    
@authRouter.post("/login",status_code=200,response_model=UserToken)
def login(
    loginDetails:UserLogin,
    session:Session=Depends(get_db)
):
    try:
        return UserService(session).login(user_details=loginDetails)
    except Exception as e:
        print(e)
        raise e