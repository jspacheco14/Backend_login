from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import User, UserRole
from app.utils.jwt_handler import create_access_token, get_current_user
from app.utils.hashing import verify_password, hash_password
from app.schemas import Token, UserLogin, CreateUserRequest

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"user_data": db_user.get_token_data()})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create-user")
def create_user(
    user_data: CreateUserRequest,
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")

    db = SessionLocal()
    existing_user = db.query(User).filter_by(username=user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    role = db.query(UserRole).filter_by(name=user_data.role).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        role_id=role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "id": str(new_user.id)}