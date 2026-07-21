from .base import BaseRepository
from ..models.resume import Resume
from typing import List

class resumeRepo(BaseRepository):
    def create_resume(
            self,
            resume:Resume
    )->Resume:
        try:
            self.session.add(resume)
            self.session.commit()
            self.session.refresh(resume)
            return resume
        except Exception:
            self.session.rollback()
            raise

    def get_resume_by_id(
            self,
            resume_id:int
    )->Resume | None:
        return self.session.query(Resume).filter(Resume.id==resume_id).first() 
    
    def get_user_resumes(
            self,
            user_id:int
    )->List[Resume]:
        return self.session.query(Resume).filter(Resume.user_id==user_id).order_by(Resume.upload_time.desc()).all()
    
    def delete_resume(
            self,
            resume_id:int
    )->bool:
        try:
            db_resume=self.get_resume_by_id(resume_id=resume_id)

            self.session.delete(db_resume)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def update_resume(
            self,
            resume:Resume
    )->Resume:
        try:
            self.session.commit()
            self.session.refresh(resume)
            return resume
        except Exception: 
            self.session.rollback()
            raise