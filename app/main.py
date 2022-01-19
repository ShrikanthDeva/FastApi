from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth ,vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins =["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#dependencies

# WHILE STRUCTURING THE API , ORDER IS IMP ie. THE PATHS GIVEN
# AS API CHECKS THE PATH SPECIFIED ONE BY ONE AND ENTERS THE ROUTE/PATH WHICH MATCHES FIRST

app.include_router(post.router) #calls the router in post.py file
app.include_router(user.router) #calls the router in user.py file
app.include_router(auth.router) #calls the router in auth.py file
app.include_router(vote.router)


# HOME PAGE
@app.get("/")   
def root():
    return {"message": "Hello World!!!!   :)"}

