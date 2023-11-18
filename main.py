from fastapi import FastAPI, Depends, HTTPException, status
from utils import verify_password, get_password_hash, create_access_token
from uuid import uuid4

from utils import create_access_token, decode_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Base
from schemas import UserCreate, UserLogin

app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Criação de uma sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.post("/create-account")
async def create_account(user_data: UserCreate):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump()
    user_data_dict['id'] = str(uuid4())
    user_data_dict['password'] = hashed_password

    user = User(**user_data_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Account successfully created"}


@app.post("/login")
async def login(user_data: UserLogin):
    db = SessionLocal()
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/secure-data")
async def secure_data(current_user: dict = Depends(decode_token)):
    return {"message": "This is secure data!", "user": current_user}
