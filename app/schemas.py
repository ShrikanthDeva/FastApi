from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

from pydantic.types import conint

# SCHEMA OF THE POST
class PostBase(BaseModel):  # class to validate the input
    title: str
    content: str
    published: bool = True
   
class PostCreate(PostBase):     # class to validate the Create input
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:   
        orm_mode = True 

# Response for the created post
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:   #converting the sqlalchemy model into pydantic model ( pydamtic model reads only a dict,our return statement is a sqlalchemy model)
        orm_mode = True #it ingones the fact that its not a dictionary and it converts it.

# SCHEMA OF THE USER
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response for the created USER

 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int

    dir: conint(le=1)


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:   
        orm_mode = True 
