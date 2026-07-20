from ..database.schemas.resume import CloudinaryUploadResult
from fastapi import UploadFile
import cloudinary.uploader
from ..core.config import settings

class CloudinaryService:
    #CONFIGURE THE SERVICE ONCE
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

    RESUME_FOLDER="ats/resumes"

    def upload_file(
            self,
            file:UploadFile,
            file_name:str,
    )->CloudinaryUploadResult:
        try:
            #clean the file_name str 
            file_name_cleaned=file_name.rsplit(".",1)[0]
            #upload the file
            cloudinary_result=cloudinary.uploader.upload(
                file.file,
                folder=self.RESUME_FOLDER,
                public_id=file_name_cleaned,
                resource_type="raw",
                overwrite=False
            )

            #Extract only the fields we need
            secure_url=cloudinary_result.get("secure_url")
            public_id=cloudinary_result.get("public_id")
            
            #return cloudinaryresponse
            return CloudinaryUploadResult(
                secure_url=secure_url,
                public_id=public_id
            )
        except Exception:
            raise 

    def delete_file(
            self,
            public_id:str
    )->dict:
        try:
            result=cloudinary.uploader.destroy(
                public_id,resource_type="raw"
            )
            return result
        except:
            raise
