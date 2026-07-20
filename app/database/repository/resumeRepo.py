from ...database.schemas.resume import ResumeResponse
from .base import BaseRepository
from ...database.models.resume import Resume
from typing import List
from datetime import datetime,timezone

class ResumeRepo(BaseRepository):
    def create_resume(
            self,
            db_resume:Resume
    )->Resume:
        try:
            self.session.add(db_resume)
            self.session.commit()
            self.session.refresh(db_resume)
            return db_resume
        except:
            self.session.rollback()
            raise 
    
    def get_resumes_by_user_id(
            self,
            user_id:int
    )->List[Resume]:
        return (self.session.query(Resume).filter(Resume.user_id==user_id).order_by(Resume.uploaded_at.desc()).all())
    
    def get_resume_by_id(
            self,
            resume_id:int
    )->Resume | None:
        return (self.session.query(Resume).filter(Resume.id==resume_id).first())

    def update_resume(
            self,
            resume:Resume
    )->Resume:
        try:
            self.session.commit()
            self.session.refresh(resume)
            return resume
        
        except:
            self.session.rollback()
            raise 

    def delete_resume(
            self,
            resume:Resume
    )->bool:
        try:
            self.session.delete(resume)
            self.session.commit()
            
            return True
        except:
            self.session.rollback()
            raise 