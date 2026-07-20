from ...core.db import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Resume(Base):
    __tablename__="resumes"
    id=Column(Integer,nullable=False,primary_key=True,index=True)
    
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    
    original_filename=Column(String,nullable=False)
    
    stored_filename=Column(String,nullable=False,unique=True)
    
    mime_type=Column(String,nullable=False)
    
    file_size=Column(Integer,nullable=False)
    
    storage_key=Column(String,nullable=False,unique=True)
    
    storage_provider=Column(String,nullable=False)

    secure_url = Column(Text, nullable=False)
    
    uploaded_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    #to access the resumes.user
    user = relationship(
        "User",
        back_populates="resumes"
    )