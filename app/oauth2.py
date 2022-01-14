from jose import JWTError, jwt
from fastapi import Depends,status,HTTPException
from datetime import datetime, time,timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secert key
#algo
#expriation time after login 


SECERET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_accesss_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    #generating the jwt
    encoded_jwt = jwt.encode(to_encode, SECERET_KEY, algorithm= ALGORITHM)


    return encoded_jwt


#verify access token
def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECERET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception

    return token_data

    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"} )
    
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # print(user)
    return user