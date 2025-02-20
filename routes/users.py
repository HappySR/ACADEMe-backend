from fastapi import APIRouter, Depends, HTTPException
from models.user_model import UserCreate, UserLogin, UserResponse
from services.auth_service import register_user, login_user
from utils.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    """Registers a new user and returns an authentication token."""
    created_user = await register_user(user)  # Await the async function
    if not created_user:
        raise HTTPException(status_code=400, detail="User registration failed")
    return created_user

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    """Logs in an existing user and returns an authentication token."""
    logged_in_user = await login_user(user)  # Await the async function
    if not logged_in_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return logged_in_user

@router.get("/me")
async def get_current_user_details(user: dict = Depends(get_current_user)):
    """Fetches the currently authenticated user's details."""
    return {"user": user}
