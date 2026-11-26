import asyncio
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import auth_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)
 
async def get_password_hash(plain_password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash, plain_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=auth_settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
    except JWTError:
        return None