from fastapi import APIRouter,UploadFile,Depends
from ..database.schemas.resume import ResumeResponse
from ..database.models.user import User
from ..dependencies.auth import get_curr_user
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..services.resumeService import ResumeService
from ..database.repository import resumeRepo
from ..services.cloudinaryService import CloudinaryService

resumeRouter=APIRouter()

def get_resume_service(
    db:Session=Depends(get_db)
)->ResumeService:
    return ResumeService(session=db)

#Upload resume
@resumeRouter.post("/add",response_model=ResumeResponse,status_code=201)
def upload_resume(
    file:UploadFile,
    curr_user:User=Depends(get_curr_user),
    resume_service:ResumeService=Depends(get_resume_service)
):
    return resume_service.upload_resume(file=file,user_id=curr_user.id)

#Get resume by id
@resumeRouter.get("/{resume_id}",response_model=ResumeResponse,status_code=200)
def get_resume_by_id(
    resume_id:int,
    curr_user:User=Depends(get_curr_user),
    resume_service:ResumeService=Depends(get_resume_service)
):
    return resume_service.get_resume_by_id(resume_id=resume_id,user_id=curr_user.id)

#get all resumes of user
@resumeRouter.get("/",response_model=list[ResumeResponse],status_code=200)
def get_user_resumes(
    curr_user:User=Depends(get_curr_user),
    resume_service:ResumeService=Depends(get_resume_service)
):
    return resume_service.get_user_resumes(user_id=curr_user.id)

#update a resume
@resumeRouter.put("/{resume_id}",response_model=ResumeResponse,status_code=200)
def update_resume(
    resume_id:int,
    file:UploadFile,
    curr_user:User=Depends(get_curr_user),
    resume_service:ResumeService=Depends(get_resume_service)
):
    return resume_service.update_resume(resume_id=resume_id,user_id=curr_user.id,file=file)

#delete a resume
@resumeRouter.delete("/{resume_id}",status_code=200)
def delete_resume(
    resume_id:int,
    curr_user:User=Depends(get_curr_user),
    resume_service:ResumeService=Depends(get_resume_service)
):
    resume_service.delete_resume(
        user_id=curr_user.id,
        resume_id=resume_id,
    )
    return {
        "message":"Resume deleted successfully"
    }