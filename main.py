# app/main.py

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.users_routes import router as users_router
from app.auth.auth import router as auth_router
from app.config.database import engine
from app.models.user_tables import Base as UserBase
import logging  # Import the logging module

# Logging configuration
logging.basicConfig(level=logging.INFO)
# Additional logging configuration if needed

UserBase.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/")
def read_root():
    return {"message": "This is the root path"}

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, tags=["Authentication"])
