from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from ..database.repository.userRepo import UserRepo
from ..database.schemas.user import UserCreate,UserResponse,UserLogin, UserToken
from ..core.security.hashHelper import hash_password,verify_password
from ..core.security.authHelper import AuthHelper


class UserService:
    def __init__(self,session:Session):
        self.__userRepository=UserRepo(session=session)

    def signup(
            self,
            user_details:UserCreate
    )->UserResponse:
        #check if user already exists
        if self.__userRepository.check_user_by_email(email=user_details.email):
            raise HTTPException(status_code=400,detail="Please Login")
        
        #hash password
        password_hash=hash_password(user_details.hashed_password)

        #save the hash password
        user_details.hashed_password=password_hash
        return self.__userRepository.create_user(user_data=user_details)
    
    def login(
            self,
            user_details:UserLogin
    ):
        if not self.__userRepository.check_user_by_email(user_details.email):
            raise HTTPException(status_code=400,detail={"User Not Found"})
        
        #get user details
        user_data=self.__userRepository.get_user_by_email(user_details.email)

        #verify password
        if not verify_password(user_details.password,user_data.hashed_password):
            raise HTTPException(status_code=401,detail="Incorrect credentials")
        
        #generate token
        token=AuthHelper.sign_jwt(user_data.id)
        if token:
            return UserToken(token=token) #As UserToken is a pydantic model it requires keyword args
        raise HTTPException(status_code=500,detail="Unable to process request")
    
      