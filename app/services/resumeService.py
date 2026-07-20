from sqlalchemy.orm import Session
from ..database.repository.resumeRepo import ResumeRepo
from .cloudinaryService import CloudinaryService
from ..database.schemas.resume import ResumeResponse
from fastapi import UploadFile,HTTPException
from ..database.schemas.resume import CloudinaryUploadResult
from ..database.models.resume import Resume
import uuid

class ResumeService:

    def __init__(
            self,
            repo: ResumeRepo,
            cloudinary: CloudinaryService      
    ):
        self._repo=repo
        self._cloudinary=cloudinary

    def _validate_resume(
            self,
            file:UploadFile

    )-> tuple:
        #validate file
        if file.filename is None or file.filename=="":
            raise HTTPException(status_code=400,detail="No Content received")
        
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400,detail="Only pdf files are allowed")
        
        file.file.seek(0,2)
        file_size=file.file.tell()
        file.file.seek(0)
        if file_size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400,detail="File Size too large")
        
        return file, file_size
    
    def _cloudinary_upload(
            self,
            file:UploadFile
    )-> tuple:
        #generate the unique filename
        unique_id=uuid.uuid4().hex
        stored_filename=f"{unique_id}.pdf"

        #upload to cloudinary
        cloudinary_result=self._cloudinary.upload_file(file=file,file_name=stored_filename)
        
        return cloudinary_result, stored_filename

    #this endpoint uploads the resume to the cloudinary servers and saves the metadata to the resume db model
    def upload_resume(
            self,
            user_id:int,
            file:UploadFile
    )->ResumeResponse:
        
        file,file_size=self.validate_resume(file=file)

        try:
            cloudinary_result,stored_filename=self.cloudinary_upload(file=file)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Cloud storage upload failed: {str(e)}"
            )

        #build the resume orm
        resume=Resume(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type,
            file_size=file_size,
            secure_url=cloudinary_result.secure_url,
            storage_key=cloudinary_result.public_id,
            storage_provider="cloudinary"
        )

        #call repo for create_resume
        db_resume=self._repo.create_resume(resume)

        #return resumeresponse
        return ResumeResponse.model_validate(db_resume)

    #verifies if the resume id belongs to the user asking for resume
    def _get_owned_resume(
            self,
            user_id:int,
            resume_id:int
    )->Resume:
        try:
            resume=self._repo.get_resume_by_id(resume_id=resume_id)
            
            if resume is None:
                raise HTTPException(status_code=404,detail="Resume not found")
            
            if resume.user_id != user_id:
                raise HTTPException(status_code=403,detail="User Not Authorised")
            
            return resume
        except:
            raise

    #returns resume metadata for any given resumeid            
    def get_resume_by_id(
        self,
        user_id: int,
        resume_id: int
    ) -> ResumeResponse:

        resume = self.get_owned_resume(
            user_id=user_id,
            resume_id=resume_id
        )

        return ResumeResponse.model_validate(resume)
    
    #returns all the resumes uploaded by a specific user
    def get_all_resumes(
            self,
            user_id:int        
    ):
        try:
            resumes=self._repo.get_resumes_by_user_id(user_id=user_id)
            return [ResumeResponse.model_validate(resume) for resume in resumes]
        except:
            raise

    def update_resume(
            self,
            resume_id:int,
            user_id:int,
            update_file:UploadFile
    )->ResumeResponse:
        
        resume=self.get_owned_resume(user_id=user_id,resume_id=resume_id)
        
        #validate input
        file,file_size=self.validate_resume(file=update_file)

        #get the old url of the resume file saved in cloudinary
        old_public_url=resume.storage_key
        try:
            #delete from cloudinary
            self._cloudinary.delete_file(old_public_url)
        except Exception:
            # Optional: Log warning here, but proceed so an orphaned cloud file doesn't block updates
            pass

        #upload the new resume to cloudinary
        try:
            cloudinary_result, stored_filename = self.cloudinary_upload(file=file)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Cloud storage upload failed: {str(e)}"
            )
        
        # update model fields
        resume.original_filename = file.filename
        resume.stored_filename = stored_filename
        resume.mime_type = file.content_type
        resume.file_size = file_size
        resume.secure_url = cloudinary_result.secure_url
        resume.storage_key = cloudinary_result.public_id

        # persist update
        db_resume = self._repo.update_resume(resume)

        return ResumeResponse.model_validate(db_resume)



    def delete_resume(self, resume_id: int, user_id: int) -> bool:
        resume = self.get_owned_resume(user_id=user_id, resume_id=resume_id)

        # attempt to delete from cloud
        try:
            self._cloudinary.delete_file(resume.storage_key)
        except Exception:
            pass

        return self._repo.delete_resume(resume)
