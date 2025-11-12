from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from database import engine, get_db, Base
from models import User
from schemas import UserRegister, UserLogin, TokenResponse, VerifyTokenResponse, UserResponse
from auth import hash_password, verify_password, create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API", version="1.0.0")

# Enable CORS for frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Auth API is running"}


@app.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password and create user
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_pwd
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return a plain dict (avoid returning ORM object directly)
        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "created_at": new_user.created_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error registering user")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password, return JWT token."""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_dict,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during login")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/verify", response_model=VerifyTokenResponse)
def verify(token: str, db: Session = Depends(get_db)):
    """Verify a JWT token and return user info."""
    try:
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Get user from database
        user = db.query(User).filter(User.email == payload["email"]).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }

        return {
            "valid": True,
            "user": user_dict,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error verifying token")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
