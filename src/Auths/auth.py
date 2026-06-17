from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
import os

pwt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# ========== Password Hashing ==========
def hasingPassword(password:str):
    return pwt_context.hash(password)

# ======== Verify Password ==========
def verifyPassword(plainPassword:str,hashPassword:str):
    return pwt_context.verify(plainPassword,hashPassword)

# ================ Create Token ==========
def createToekn(data:dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=1)

    token = jwt.encode(
        payload,
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )

    return token

# ========= Verify Token ========
def verifyToken(token):
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=os.getenv("ALGORITHM")
        )
        return payload
    except JWTError:
        return None