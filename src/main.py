"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.db import get_engine
from src.common.base_entity import Base

app = FastAPI(root_path="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """
    Creates database tables on application startup.
    """
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
