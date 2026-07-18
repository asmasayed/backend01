from pydantic import BaseModel, EmailStr,ConfigDict

class UserBase(BaseModel):
    name:str
    email:EmailStr

class UserCreate(UserBase):
    hashed_password:str

class UserResponse(UserBase):
    id:int
    #Enable your UserResponse to read dbmodels from db
    model_config=ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserToken(BaseModel):
    token:str