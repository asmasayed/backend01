#database user model

from sqlalchemy import Column,Integer,String
from ...core.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    hashed_password=Column(String,nullable=False)
    role=Column(String,nullable=False,server_default="user")

    #to access all resumes for a user 
    resumes=relationship(
        "Resume",
        #whenever I change something on the User side, immediately update the Resume side in Python memory too (and vice versa)
        back_populates="user",
        #User owns the resume, if the resume is disconnected from the user, delete the resume 
        cascade="all, delete-orphan"
    )