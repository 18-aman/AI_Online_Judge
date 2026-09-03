from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI-Powered Online Judge API",
    description="Backend API for the Online Judge & Intelligent Coding Platform",
    version="1.0.0",
)

# Configure CORS for frontend access
origins = [
    "http://localhost:5173", # Vite dev server
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.auth import router as auth_router
from app.api.problems import router as problems_router
from app.api.admin import router as admin_router
from app.api.leaderboard import router as leaderboard_router
from app.api.recommendations import router as recommendations_router
from app.api.users import router as users_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(problems_router, prefix="/problems", tags=["problems"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["leaderboard"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["recommendations"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running securely"}
