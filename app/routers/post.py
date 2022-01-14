from app import oauth2
from .. import models,schemas,oauth2
from typing import List, Optional  # optional rating field
from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from  sqlalchemy import func # for counting

router = APIRouter(
    prefix="/posts",    #prefix route path for all the posts
    tags=['Posts']  #grouping
)


# ----- CRED API ------  C -create   R -read  E -edit/update  D - delete --------------



#DISPLAYS ALL THE POST
@router.get("/",response_model=List[schemas.PostOut])    #list of posts
def get_Posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0,search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Getting the count of votes by doung the left outer join with votes and post table (using post_id common feild) and grouping it by Post_id and filter acc to the search needed
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts


#CREATES A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # Inefficient way of creating a post ie. for 50 columns in table we cant proceed like the below way
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    # better approach is to convert to dict and pass it
     
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)    #add to db  
    db.commit()         #save in db
    db.refresh(new_post)    # returning * command
    return new_post
#title str, content str



#DISPLAYS THE POST WITH THE GIVEN ID
@router.get("/{id}",response_model=schemas.PostOut) # id here in url is  path parameter
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #,response: Response #validates the id (is its changeable to int) and type casted to int as the url gets it as the string
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:    # if post not found we change the status code to 404 error not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the ID : {id} was not found")

        # Other big method to raise the exception
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"meessage": f"Post with the ID : {id} was not found"}

    return post

#DELETE A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
             detail=f"Post with the ID : {id} Doesnt exist ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authoraised to perform required option")

    #return {"MESSAGE": "Post was successfully deleted"} You cant send data back when u give 204 error
    post_query.delete(synchronize_session=False)  # most releiable option
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#UPDATES A POST
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""", (post.title,post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post  = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
             detail=f"Post with the ID : {id} Doesnt exist ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authoraised to perform required option")


    post_querry.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_querry.first()
