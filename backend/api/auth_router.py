from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import database, models
from auth import schemas, security

router = APIRouter()

class FirebaseLoginRequest(schemas.BaseModel):
    email: str

@router.post("/firebase-login", response_model=schemas.User)
def firebase_login(request: FirebaseLoginRequest, token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        # Decode the Firebase token to get the actual email from the provider
        current_user_token = security.verify_firebase_token(token)
        token_email = current_user_token.get("email")
        
        if not token_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no email found")
            
        # Check if user exists locally
        user = security.get_user_by_email(db, email=token_email)
        
        if not user:
            # First time Google Sign-in: Auto-provision as Admin
            user = models.User(
                email=token_email,
                hashed_password="firebase_managed",
                role="Admin",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        return user
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication server error: {str(e)}")

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_active_user)):
    return current_user
