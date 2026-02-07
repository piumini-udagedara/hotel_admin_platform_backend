from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine, Base
from app.models import User, Hotel, RoomType, RateAdjustment  # noqa: F401
from app.api import auth, hotels, room_types

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(room_types.router)


@app.get("/")
def root():
    return {"message": "Hotel Admin Platform API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}