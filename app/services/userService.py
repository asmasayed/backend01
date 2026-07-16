from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from ..database.repository.userRepo import UserRepo
from ..database.schemas.user import UserCreate,UserResponse
from ..core.security.hashHelper import hash_password


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
