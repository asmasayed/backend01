from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..core.db import get_db
from ..database.models.user import User
from ..core.security.authHelper import oauth2_scheme, AuthHelper
from ..database.repository.userRepo import UserRepo
from jose import JWTError

def get_curr_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
)->User:
    credentials_exception=HTTPException(status_code=401,detail="Cannot validate credentials")
    try:
        #Decodes and verifies the JWT.
        payload=AuthHelper.decode_jwt(token)
        
        #Extracts the user Id.
        user_id:str=payload.get("sub")
        if user_id is None:
            raise credentials_exception

    
        #Fetches the user from the database (via UserRepo) to ensure the account still exists and isn't banned.
        db_user=UserRepo(session=db).get_user_by_id(int(user_id))

        if db_user is None:
            raise credentials_exception
    
        #Returns the full database user object.
        return db_user
    except JWTError as e:
        raise credentials_exception