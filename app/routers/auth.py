from ..database.schemas.user import UserResponse,UserCreate,UserToken,UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..core.db import get_db
from ..services.userService import UserService
from ..dependencies.roleChecker import RoleChecker
from fastapi.security import OAuth2PasswordRequestForm

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
    form_data:OAuth2PasswordRequestForm=Depends(),
    session:Session=Depends(get_db)
):
    try:
        return UserService(session).login(form_data=form_data)
    except Exception as e:
        print(e)
        raise e
    
@authRouter.get("/admin-dashboard",status_code=200)
def admin_dashboard(
    admin=Depends(RoleChecker(["admin"]))
):
    return {"message": f"Welcome to the bridge, Admin {admin.email}"}

@authRouter.get("/user-dashboard",status_code=200)
def user_dashboard(
    user=Depends(RoleChecker(["user"]))
):
    return {"message":f"Welcome, User {user.name}"}