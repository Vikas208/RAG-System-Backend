from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes.auth import router as authRouter
from app.routes.upload import router as uploadRouter
from app.routes.websocket import router as websocketRouter
import os

load_dotenv()
# Make uplaod directory if not exist

DIRECTORY_PATH = os.getenv("UPLOAD_PATH")
if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)


app = FastAPI(title="RAG API", version="1.0.0")


# CORS MIDDLEWARE
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(authRouter,tags=['auth'],prefix="/api/v1")
app.include_router(uploadRouter,tags=['upload'],prefix="/api/v1")
app.include_router(websocketRouter,tags=['websocket'])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return error_response(
        message="An unexpected error occurred",
        status_code=500,
        details=str(exc)
    )
