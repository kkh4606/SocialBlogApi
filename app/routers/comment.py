
from app import  schemas,database, oauth2, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

router = APIRouter(prefix="/posts", tags=["POST"])






@router.post("/comment/{post_id}", status_code=status.HTTP_201_CREATED, response_model = schemas.CommentOut)
def post_comment(
    post_id: int,
    comment: schemas.Comment,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = models.Comment(**comment.model_dump(), owner_id=current_user.id, post_id=post_id)  # type:ignore
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return  new_comment


    # return {
    #     "id": new_comment.id,
    #     "content": new_comment.content,
    #     'owner_id': new_comment.owner_id,
    #     'post_id': new_comment.post_id,
    #     'created_at': new_comment.created_at,
    #
    #     'post' :  {
    #         'id' : post_id,
    #         'content' : post.content,
    #         'title' : post.title,
    #         'owner_id' : post.owner_id,
    #         'created_at' : post.created_at,
    #
    #     },
    #     'owner' : {
    #         'id' : current_user.id,
    #         'name' : current_user.name,
    #         'email' : current_user.email,
    #         'created_at' : current_user.created_at
    #     }
    # }