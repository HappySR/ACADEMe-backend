from pydantic import BaseModel, EmailStr
import datetime

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    student_class: str  # ✅ Added to store the class of the student
    name: str

class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response after successful login/registration."""
    email: EmailStr
    token: str
    student_class: str  # ✅ Include class in the response
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Duration for which the token is valid (in seconds)
    created_at: datetime.datetime  # Timestamp of when the token was created
    email: EmailStr  # Add email here if needed in the response
    student_class: str  # Include class in the token response as well

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
