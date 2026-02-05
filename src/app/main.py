import os
import shutil
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from services.voice_changer import voice_changer

load_dotenv()

app = FastAPI()

UPLOAD_DIR = os.getenv("INPUT_FILES_PATH")
OUTPUT_DIR = os.getenv("OUTPUT_FILES_PATH")

GIRL = os.getenv("GIRL_ID")
BOY = os.getenv("BOY_ID")
MAN = os.getenv("MAN_ID")
WOWAN = os.getenv("WOWAN_ID")

os.makedirs(UPLOAD_DIR, exist_ok = True)
os.makedirs(OUTPUT_DIR, exist_ok = True)

@app.get("/")
async def root():
    return {"message": "Welcome to Voice Changer!"}

@app.post("v1/voice_changer/services/change_voice")
async def change_voice(
    file: Annotated[UploadFile, File(description = "A file read as UploadFile")]
):
    """Change your voice for any purpose. 

    Args:
        file (must be an audio file) - audio to voice change. Defaults to "A file read as UploadFile")].

    Returns:
        Dict - metadata
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        voice_changed = voice_changer(
            voice_id = MAN,
            audio_url = file_path
        )
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
    finally:
        await file.close()
    
    return {"filename_uploaded": file.filename, "content_type": file.content_type, "message": "File uploaded successfully", "output": voice_changed}