from fastapi import FastAPI
from app.database import engine

from app import models
from app.routers import user, post, auth, vote, image_upload, comment
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(auth.router, tags=["authentication"])

app.include_router(comment.router)

app.include_router(vote.router)
app.include_router(image_upload.router)


@app.get("/", include_in_schema=False)
def hello():
    return {"message": "Hello, World"}
