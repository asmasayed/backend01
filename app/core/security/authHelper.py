from ..config import settings 
from jose import jwt
import time
from ...database.models.user import User
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

class AuthHelper(object):

    #Generate token
    @staticmethod
    def sign_jwt(user_data:User)->str:
        payload={
            "sub":str(user_data.id),
            "user_role":user_data.role,
            "expires":time.time()+900
        }
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token
    
    def decode_jwt(token:str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])