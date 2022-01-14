from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy import schema
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database,schemas,models,utils,oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model= schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):

    #OAuth2PasswordRequestForm sstores the given input as dict of {"username": "xxx", "password": "yyy"} so we user username instead of email
    user= db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    #create a token & return token
    access_token = oauth2.create_accesss_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer" }