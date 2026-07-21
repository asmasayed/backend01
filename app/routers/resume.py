from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..database.models.user import User
from ..database.repository.resumeRepo import ResumeRepo
from ..database.schemas.resume import ResumeResponse
from ..dependencies.auth import get_curr_user
from ..services.cloudinaryService import CloudinaryService
from ..services.resumeService import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["Resume"],
)


def get_resume_service(
    db: Session = Depends(get_db),
) -> ResumeService:
    repo = ResumeRepo(db)
    cloudinary = CloudinaryService()
    return ResumeService(
        repo=repo,
        cloudinary=cloudinary,
    )


@router.post(
    "/",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_curr_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.upload_resume(
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "/",
    response_model=list[ResumeResponse],
    status_code=status.HTTP_200_OK,
)
def get_user_resumes(
    current_user: User = Depends(get_curr_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_user_resumes(
        user_id=current_user.id,
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK,
)
def get_resume_by_id(
    resume_id: int,
    current_user: User = Depends(get_curr_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_resume_by_id(
        user_id=current_user.id,
        resume_id=resume_id,
    )


@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK,
)
def update_resume(
    resume_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_curr_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.update_resume(
        user_id=current_user.id,
        resume_id=resume_id,
        file=file,
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_curr_user),
    service: ResumeService = Depends(get_resume_service),
):
    service.delete_resume(
        user_id=current_user.id,
        resume_id=resume_id,
    )
    return {
        "message": "Resume deleted successfully"
    }