from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_db
from routers import videos, categories, comments
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(
    title="Streaming Platform API",
    description="API de plataforma de streaming con FastAPI, SQLModel y AWS S3",
    version="1.0.0",
    lifespan=lifespan 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api"


app.include_router(videos.router, prefix=api_prefix, tags=["Videos"])
app.include_router(categories.router, prefix=api_prefix, tags=["Categories"])
app.include_router(comments.router, prefix=api_prefix, tags=["Comments"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Streaming API is running"}