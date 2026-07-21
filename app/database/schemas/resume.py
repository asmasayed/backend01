from pydantic import BaseModel,ConfigDict
from datetime import datetime

class ResumeResponse(BaseModel):
    id:int
    user_id:int
    original_filename:str
    stored_filename:str
    file_size:int
    mime_type:str

    public_id:str
    secure_url:str

    upload_time:datetime
    update_time:datetime

    model_config=ConfigDict(
        from_attributes=True,  # Enables reading from SQLAlchemy ORM objects
    )

class CloudinaryUploadResponse(BaseModel):
    secure_url:str
    public_id:str