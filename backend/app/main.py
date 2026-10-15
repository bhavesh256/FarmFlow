from contextlib import asynccontextmanager
from app.routes.users import router as users_router

from fastapi import FastAPI, Request
from app.db.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb(app)
    yield
    await close_mongodb_connection(app)


app = FastAPI(title="FarmFlow API", lifespan=lifespan)

app.include_router(users_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "FarmFlow API is running"}


@app.get("/health/db")
async def database_health(request: Request):
    await request.app.state.db.command("ping")
    return {"database": "connected"}
