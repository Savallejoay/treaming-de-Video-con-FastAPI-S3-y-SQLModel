from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, func
from db import engine
from models import Video, Comment
from typing import List

router = APIRouter()

@router.get("/videos", response_model=List[Video])
def get_videos():
    with Session(engine) as session:
        videos = session.exec(select(Video)).all()
        return videos

@router.get("/videos/{video_id}")
def get_video(video_id: int):
    with Session(engine) as session:
       
        video = session.get(Video, video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video no encontrado")
        
        return video

@router.get("/videos/recommendations/{category_id}")
def get_recommendations(category_id: int):
    with Session(engine) as session:
        
        statement = (
            select(Video)
            .where(Video.category_id == category_id)
            .order_by(func.random())
            .limit(10)
        )
        results = session.exec(statement).all()
        return results

@router.post("/videos", response_model=Video)
def create_video(video: Video):
    with Session(engine) as session:

        video.id = None 
        session.add(video)
        session.commit()
        session.refresh(video)
        return video

@router.get("/videos/category/{category_id}")
def get_videos_by_category(category_id: int):
    with Session(engine) as session:
        videos = session.exec(
            select(Video).where(Video.category_id == category_id)
        ).all()
        return videos