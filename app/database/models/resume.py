from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from ...core.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Resume(Base):
    __tablename__="resumes"
    id=Column(Integer,nullable=False,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    original_filename=Column(String,nullable=False)
    stored_filename=Column(String,nullable=False)
    file_size=Column(Integer,nullable=False)
    mime_type=Column(String,nullable=False)

    #cloudinary related storage variables
    public_id=Column(String,nullable=False,unique=True)
    secure_url=Column(Text,nullable=False)

    #time related info
    upload_time=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    update_time=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

    #relationship, that tells sqlalc that this resume belongs to one 'User' adn links it to the 'resumes' for that user
    #creating a link Resume->User 
    user=relationship(
        "User",
        back_populates="resumes"
    )