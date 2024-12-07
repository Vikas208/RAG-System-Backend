from fastapi import FastAPI, Request
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

app = FastAPI()
app.include_router(authRouter,tags=['auth'])
app.include_router(uploadRouter,tags=['upload'])
app.include_router(websocketRouter,tags=['websocket'])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return error_response(
        message="An unexpected error occurred",
        status_code=500,
        details=str(exc)
    )