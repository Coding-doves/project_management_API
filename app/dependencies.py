from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from app import db, model, schemas

SECRET_KEY = "blog"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_passwd(plain_password: str, db_hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_password, db_hashed_pwd)

def create_access_token(data: dict, expires: timedelta = None) -> str:
    encode = data.copy()
    if expires:
        exp = datetime.utcnow() + expires
    else:
        exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    encode.update({"exp": exp})
    encode_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

def get_db():
    db_instance = db.get_db()
    try:
        yield db_instance
    finally:
        db_instance.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    user = db.query(model.User).filter(model.User.username == payload.get("sub")).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(user: schemas.User = Depends(get_current_user)) -> schemas.User:
    if not user.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

def get_current_active_admin(user: schemas.User = Depends(get_current_active_user)) -> schemas.User:
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user

def get_current_active_guest(user: schemas.User = Depends(get_current_active_user)) -> schemas.User:
    if not any(role.name == "guest" for role in user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user
