from .base import BaseRepository
from ..schemas.user import UserCreate
from ..models.user import User
class UserRepo(BaseRepository):
    def create_user(
            self,
            user_data:UserCreate
    ):
        #convert UserCreate into python dict
        #newUser becomes an sqlalchemy model instance
        newUser=User(**user_data.model_dump(exclude_none=True))
        self.session.add(instance=newUser)
        self.session.commit()
        self.session.refresh(instance=newUser)

        return newUser
    
    def check_user_by_email(
            self,
            email:str
    )->bool:
        user=self.session.query(User).filter(User.email==email).first()
        return bool(user)
    
    def get_user_by_email(
            self,
            email:str
    )->User:
        user=self.session.query(User).filter(User.email==email).first()
        return user
    
    def get_user_by_id(
            self,
            id:int
    )->User:
        user=self.session.query(User).filter(User.id==id).first()
        return user   
 