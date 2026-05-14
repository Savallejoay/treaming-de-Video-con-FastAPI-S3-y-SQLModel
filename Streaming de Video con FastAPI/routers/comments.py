from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Comment, Video
from typing import List

router = APIRouter()

@router.get("/comments/{video_id}", response_model=List[Comment])
def get_comments(video_id: int):
    with Session(engine) as session:
        statement = select(Comment).where(Comment.video_id == video_id)
        comments = session.exec(statement).all()
        return comments

@router.post("/comments", response_model=Comment)
def create_comment(comment: Comment):
    with Session(engine) as session:
        video = session.get(Video, comment.video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video no encontrado")
        if not comment.content or not comment.content.strip():
            raise HTTPException(status_code=400, detail="El contenido del comentario no puede estar vacío")

        comment.id = None
        comment.content = comment.content.strip()

        session.add(comment)
        session.commit()
        session.refresh(comment)

        return comment