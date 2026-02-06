import os
import shutil
from dotenv import load_dotenv
from typing import Annotated, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from services.voice_changer import voice_changer
from models.menu import menu_choices
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

UPLOAD_DIR = os.getenv("INPUT_FILES_PATH")
OUTPUT_DIR = os.getenv("OUTPUT_FILES_PATH")

GIRL = os.getenv("GIRL_ID")
BOY = os.getenv("BOY_ID")
MAN = os.getenv("MAN_ID")
WOMAN = os.getenv("WOMAN_ID")

os.makedirs(UPLOAD_DIR, exist_ok = True)
os.makedirs(OUTPUT_DIR, exist_ok = True)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # deixe False se não usa cookies/sessão
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Voice Changer!"}

@app.post("/v1/voice_changer/services/voice_change")
async def change_voice(
    file: Annotated[UploadFile, File(description = "A file read as UploadFile")],
    menu_item: Union[menu_choices] 
):
    """Change your voice for any purpose. 

    Args:
        file (must be an audio file) - audio to voice change.
        menu_item - voice options

    Returns:
        Dict - metadata
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if menu_item == menu_choices.girl:
            voice = GIRL
        elif menu_item == menu_choices.boy:
            voice = BOY
        elif menu_item == menu_choices.woman:
            voice = WOMAN
        elif menu_item == menu_choices.man:
            voice = MAN
        
        voice_changed = voice_changer(
            voice_id = voice,
            audio_url = file_path
        )

    except Exception as e:
        return {"message": f"An error occurred: {e}"}
    finally:
        await file.close()
    
    return {
        "filename_uploaded": file.filename, 
        "content_type": file.content_type, 
        "message": "File uploaded successfully", 
        "output": voice_changed
    }

@app.get("/v1/voice_changer/services/get_audio_response", response_class = FileResponse)
async def get_audio():
    try:
        audio = os.getenv("AUDIO_RESPONSE")
        return audio
    except Exception as e:
        return {"message": f"An error occurred: {e}"}
    
