import uuid

from fastapi import HTTPException, UploadFile

from ..database.models.resume import Resume
from ..database.repository.resumeRepo import ResumeRepo
from ..database.schemas.resume import ResumeResponse
from .cloudinaryService import CloudinaryService


class ResumeService:

    def __init__(
        self,
        repo: ResumeRepo,
        cloudinary: CloudinaryService,
    ):
        self._repo = repo
        self._cloudinary = cloudinary

    def _validate_resume(
        self,
        file: UploadFile,
    ) -> tuple[UploadFile, int]:

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file uploaded."
            )

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size cannot exceed 5 MB."
            )

        return file, file_size

    def _cloudinary_upload(
        self,
        file: UploadFile,
    ):

        unique_id = uuid.uuid4().hex
        stored_filename = f"{unique_id}.pdf"

        cloudinary_result = self._cloudinary.upload_file(
            file=file,
            file_name=stored_filename,
        )

        return cloudinary_result, stored_filename

    def _get_owned_resume(
        self,
        user_id: int,
        resume_id: int,
    ) -> Resume:

        resume = self._repo.get_resume_by_id(resume_id)

        if resume is None:
            raise HTTPException(
                status_code=404,
                detail="Resume not found."
            )

        if resume.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this resume."
            )

        return resume

    # Upload a new resume
    def upload_resume(
        self,
        user_id: int,
        file: UploadFile,
    ) -> ResumeResponse:

        file, file_size = self._validate_resume(file)

        try:
            cloudinary_result, stored_filename = self._cloudinary_upload(file)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Cloud storage upload failed: {str(e)}"
            )

        resume = Resume(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type,
            file_size=file_size,
            storage_key=cloudinary_result.public_id,
            secure_url=cloudinary_result.secure_url,
            storage_provider="cloudinary",
        )

        db_resume = self._repo.create_resume(resume)

        return ResumeResponse.model_validate(db_resume)

    # Get a specific resume
    def get_resume_by_id(
        self,
        user_id: int,
        resume_id: int,
    ) -> ResumeResponse:

        resume = self._get_owned_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        return ResumeResponse.model_validate(resume)

    # Get all resumes uploaded by the current user
    def get_user_resumes(
        self,
        user_id: int,
    ) -> list[ResumeResponse]:

        resumes = self._repo.get_resumes_by_user_id(user_id)

        return [
            ResumeResponse.model_validate(resume)
            for resume in resumes
        ]

    # Replace an existing resume
    def update_resume(
        self,
        user_id: int,
        resume_id: int,
        file: UploadFile,
    ) -> ResumeResponse:

        resume = self._get_owned_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        file, file_size = self._validate_resume(file)

        old_public_id = resume.storage_key

        try:
            cloudinary_result, stored_filename = self._cloudinary_upload(file)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Cloud storage upload failed: {str(e)}"
            )

        resume.original_filename = file.filename
        resume.stored_filename = stored_filename
        resume.mime_type = file.content_type
        resume.file_size = file_size
        resume.storage_key = cloudinary_result.public_id
        resume.secure_url = cloudinary_result.secure_url

        db_resume = self._repo.update_resume(resume)

        try:
            self._cloudinary.delete_file(old_public_id)
        except Exception:
            pass

        return ResumeResponse.model_validate(db_resume)

    # Delete a resume
    def delete_resume(
        self,
        user_id: int,
        resume_id: int,
    ) -> bool:

        resume = self._get_owned_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        try:
            self._cloudinary.delete_file(resume.storage_key)
        except Exception:
            pass

        return self._repo.delete_resume(resume)