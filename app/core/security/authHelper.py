from ..config import settings 
from jose import jwt
import time

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM

class AuthHelper(object):

    #Generate token
    @staticmethod
    def sign_jwt(id:int)->str:
        payload={
            "user_id":id,
            "expires":time.time()+900
        }
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return token