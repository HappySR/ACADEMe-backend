from firebase_admin import auth, firestore
from models.user_model import UserCreate, UserLogin, TokenResponse
from utils.auth import create_jwt_token
from fastapi import HTTPException

db = firestore.client()

async def register_user(user: UserCreate) -> TokenResponse:
    """Registers a user in Firebase Auth & Firestore."""
    try:
        # Create user in Firebase Auth
        user_record = auth.create_user(email=user.email, password=user.password)
        
        # Store user data in Firestore
        user_data = {
            "id": user_record.uid,
            "name": user.name,
            "email": user.email,
            "class": user.student_class,  # Stores the student's class
        }
        db.collection("users").document(user_record.uid).set(user_data)

        # Generate JWT token
        token = create_jwt_token(user_record.uid)
        return TokenResponse(access_token=token, token_type="bearer")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def login_user(user: UserLogin) -> TokenResponse:
    """Verifies user login credentials and returns a JWT token."""
    try:
        user_record = auth.get_user_by_email(user.email)
        
        # Generate JWT token
        token = create_jwt_token(user_record.uid)
        return TokenResponse(access_token=token, token_type="bearer")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
