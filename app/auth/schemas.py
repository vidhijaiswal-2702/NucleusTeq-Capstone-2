from datetime import datetime
from typing import Union
from app.auth.base import BaseResponse
from pydantic import BaseModel, EmailStr, Field, field_validator # type: ignore
from app.auth.roles import UserRole

# register user request schema
class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    @field_validator('email')
    def validate_email(cls, v):
        if not v.endswith('@gmail.com'):
            raise ValueError('Email must end with @gmail.com')
        return v
    password: str
    role: UserRole
    
class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr

# user response schema    
class UserResponse(BaseResponse):
    # id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool 
    created_at: Union[str,None,datetime] = None 
    
   #login response  
class LoginResponse(BaseResponse):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer" 
    
class VerifyUserRequest(BaseModel):
    token:str
    email:EmailStr
    
class EmailRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    password: str 
    token: str
    
    