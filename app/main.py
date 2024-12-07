from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.auth import router as authRouter
from app.routes.upload import router as uploadRouter
import os

load_dotenv()
# Make uplaod directory if not exist 

DIRECTORY_PATH = os.getenv("UPLOAD_PATH")
if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)

app = FastAPI()
app.include_router(authRouter,tags=['auth'])
app.include_router(uploadRouter,tags=['upload'])




