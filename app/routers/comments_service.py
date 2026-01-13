from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Comment


def structure_comments(comments: List[Comment]) -> List[Comment]:
    comment_map = {}

    # init replies + map
    for comment in comments:
        comment.replies = []
        comment_map[comment.id] = comment

    root_comments = []

    for comment in comments:
        if comment.parent_id is not None:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.replies.append(comment)
        else:
            root_comments.append(comment)

    return root_comments
def get_comments_by_post_id(
    post_id: int,
    db: Session
) -> List[Comment]:

    comments = db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
    ).scalars().all()

    return structure_comments(comments)


def create_comment(
    content: str,
    user_id: int,
    post_id: int,
    db: Session,
    parent_id: Optional[int] = None
) -> Comment:

    if parent_id == 0:
        parent_id = None

    print(parent_id)

    comment = Comment(
        content=content,
        owner_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment
