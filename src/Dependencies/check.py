from fastapi.security import HTTPBearer
from fastapi import HTTPException,Depends
from src.Auths.auth import verifyToken

security = HTTPBearer()

def isLogin(token=Depends(security)):
    data = verifyToken(token.credentials)
    if not data:
        raise HTTPException(401,detail="Invalid Token")
    
    return data