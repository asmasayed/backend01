import cloudinary
from ..core.config import settings
from fastapi import UploadFile
from ..database.schemas.resume import CloudinaryUploadResponse
import cloudinary.uploader

class CloudinaryService:
    def __init__(self):
        #config the service once at the start
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
            file_name:str
    )->CloudinaryUploadResponse:
        try:
            cloudinary_result=cloudinary.uploader.upload(
                file.file,
                folder=self.RESUME_FOLDER,
                public_id=file_name,
                resource_type="raw",
                overwrite=False
            )

            return CloudinaryUploadResponse(
                secure_url=cloudinary_result.get("secure_url"),
                public_id=cloudinary_result.get("public_id")
            )
        except Exception:
            raise

    def delete_file(
            self,
            public_id:str
    )->dict:
        try:
            return cloudinary.uploader.destroy(
                public_id=public_id,
                resource_type="raw"
            )
        except Exception:
            raise