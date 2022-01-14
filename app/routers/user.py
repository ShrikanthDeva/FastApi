from .. import models,schemas,utils
from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# ------ USER -----------

#CREATES A User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    
    #hash the password - user.password
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)    #add to db  
    db.commit()         #save in db
    db.refresh(new_user)    # returning * command
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id: {id} Does not exist")

    return user