from sqlalchemy.orm import Session
from ..database.repository.resumeRepo import resumeRepo
from fastapi import UploadFile,HTTPException
from ..database.schemas.resume import ResumeResponse,CloudinaryUploadResponse
from .cloudinaryService import CloudinaryService
from ..database.models.resume import Resume
from typing import List
import uuid

class ResumeService:
    def __init__(self,session:Session):
        self._resumeRepository=resumeRepo(session=session)
        self._cloudinaryService=CloudinaryService()

    def _validate_file(
            self,
            file:UploadFile
    )->int:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file found"
            )
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only pdf upload is supported"
            )
        file.file.seek(0,2)
        file_size= file.file.tell()
        file.file.seek(0)

        if file_size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size should be less than 5 MB"
            )
        return file_size

    def _generate_filename(
            self
    )->str:
        unique_id=uuid.uuid4().hex[:8]
        return f"{unique_id}.pdf"

    def upload_resume(
            self,
            file:UploadFile,
            user_id:int
    )->ResumeResponse:
        
        #Validate the user uploaded file
        file_size=self._validate_file(file)
        stored_filename=self._generate_filename()

        #upload to cloudinary
        cloudinary_result:CloudinaryUploadResponse=self._cloudinaryService.upload_file(
            file=file,
            file_name=stored_filename.rsplit(".",1)[0]
        )

        #upload to db
        resume=Resume(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_size=file_size,
            mime_type=file.content_type,
            public_id=cloudinary_result.public_id,
            secure_url=cloudinary_result.secure_url
        )

        db_resume=self._resumeRepository.create_resume(resume=resume)

        return ResumeResponse.model_validate(db_resume)

    def get_resume_by_id(
            self,
            resume_id:int,
            user_id:int
    )->Resume:
        resume=self._resumeRepository.get_resume_by_id(resume_id=resume_id)
            
        if resume is None:
            raise HTTPException(
                status_code=404,
                detail="Resume not Found"
            )

        if user_id != resume.user_id:
            raise HTTPException(
                status_code=403,
                detail="Not Authorised"
            )
        return resume
        

    def get_user_resumes(
            self,
            user_id:int
    )->List[ResumeResponse]:
        resumes=self._resumeRepository.get_user_resumes(user_id=user_id)
        return [
            ResumeResponse.model_validate(resume)
            for resume in resumes
        ]
    
    def delete_resume(
            self,
            resume_id:int,
            user_id:int
    )->bool:
        
        resume=self.get_resume_by_id(resume_id=resume_id,user_id=user_id)

        #delete resume from cloudinary
        self._cloudinaryService.delete_file(public_id=resume.public_id)

        #delete from db
        return self._resumeRepository.delete_resume(resume_id)
    
    def update_resume(
            self,
            resume_id:int,
            user_id:int,
            file:UploadFile
    )->ResumeResponse:
         
        resume=self.get_resume_by_id(resume_id=resume_id,user_id=user_id)
        
        #validate the new resume
        file_size=self._validate_file(file=file)

        #generate a new file name
        stored_filename=self._generate_filename()

        #extract the old public_id to delete it later
        old_public_id=resume.public_id

        #upload the new file to cloudinary
        cloudinary_result=self._cloudinaryService.upload_file(file=file,file_name=stored_filename)

        try:
            #update db values
            resume.original_filename=file.filename
            resume.stored_filename=stored_filename
            resume.file_size=file_size
            resume.mime_type=file.content_type
            resume.public_id=cloudinary_result.public_id
            resume.secure_url=cloudinary_result.secure_url

            #update the resume in db
            db_resume=self._resumeRepository.update_resume(resume)

            #delete old resume from cloudinary
            result=self._cloudinaryService.delete_file(public_id=old_public_id)

            return ResumeResponse.model_validate(db_resume)
        except Exception as e:
            if cloudinary_result and cloudinary_result.public_id:
                self._cloudinaryService.delete_file(
                    public_id=cloudinary_result.public_id
                )
                raise e