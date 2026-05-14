from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    videos: List["Video"] = Relationship(back_populates="category")


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    thumbnail_url: str
    video_url: str

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    category: Optional[Category] = Relationship(back_populates="videos")
    
    comments: List["Comment"] = Relationship(
        back_populates="video", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    content: str

    video_id: Optional[int] = Field(default=None, foreign_key="video.id")

    video: Optional[Video] = Relationship(back_populates="comments")