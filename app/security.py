from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = "NT-LIBARARY-SECRET-KEY"


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_token(data: dict) -> str:
    payload = data.copy()

    token = jwt.encode(payload, secret, algorithm="HS256")

    return token


def verify_token(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token.")

    return decoded_payload
