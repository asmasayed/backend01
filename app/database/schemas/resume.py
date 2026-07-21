from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime
from typing import Optional

class ResumeCreate(BaseModel):
    user_id: int
    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    storage_key: str
    storage_provider: str

class ResumeUpdate(BaseModel):
    name: Optional[str] = None

#What details does the frontend need for a resume to show(metadata)
class ResumeResponse(BaseModel):
    id:int
    user_id:int
    name:str=Field(validation_alias="original_filename") #since pydantic expects schema name and db name to be same for 'form attributes'
    stored_filename:str
    mime_type:str
    file_size:int
    storage_provider:str
    secure_url: str
    uploaded_at: datetime

    #Enable your ResumeResponse to read dbmodels from db
    model_config=ConfigDict(from_attributes=True)

class ResumeUploadResponse(BaseModel):
    message:str
    resume:ResumeResponse

class CloudinaryUploadResult(BaseModel):
    #returns metadata that was saved in db
    secure_url:str
    public_id:str