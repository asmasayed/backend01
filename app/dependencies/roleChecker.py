from fastapi import Depends, HTTPException
from ..database.models.user import User
from .auth import get_curr_user

class RoleChecker:
    def __init__(self,allowed_roles:list[str]):
        self.allowed_roles=allowed_roles

    def __call__(self, curr_user:User=Depends(get_curr_user)):
        if curr_user.role not in self.allowed_roles:
            raise HTTPException(status_code=403,detail="Permission Denied")
        return curr_user