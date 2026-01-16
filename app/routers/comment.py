from sqlalchemy.sql.functions import current_user

from app import schemas, database, oauth2, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from app.routers.comments_service import create_comment

router = APIRouter(tags=["comments"])


@router.get("/comments", response_model=List[schemas.CommentOut])
def get_comments(
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):

    comments = db.query(models.Comment).filter(models.Comment.parent_id == None).all()

    return comments


@router.post(
    "/comments/{post_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentOut,
)
def post_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    new_comment = create_comment(
        content=comment.content,
        user_id=current_user.id,
        post_id=post_id,
        parent_id=comment.parent_id,
        db=db,
    )

    return new_comment


@router.post(
    "/comments/{comment_id}/replies",
    response_model=schemas.CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def reply_comment(
    comment_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    parent_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )

    if not parent_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    reply = models.Comment(
        content=comment.content,
        owner_id=current_user.id,
        parent_id=parent_comment.id,
        post_id=parent_comment.post_id,
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)

    return reply


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if current_user.id != comment.owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to perform request acton",
        )

    db.delete(comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/comments/{comment_id}")
def update_comment(
    comment_id: int,
    comment_update: schemas.EditComment,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):

    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if current_user.id != comment.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permission to perform request acton",
        )

    comment.content = comment_update.content
    db.commit()
    db.refresh(comment)
    return comment
