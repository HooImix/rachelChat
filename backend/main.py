 #* uvicorn main:app
 #* uvicorn main:app --reload

#// Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai


#// Custom Functions Imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

#// Initiate App
app = FastAPI()


#// CORS - Origins
orgins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:8000",
]


#// CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#// Check API health
@app.get("/green")
async def green():
    return {"status": "green"}

#/// Reset endpoint
#// Reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation reset"}



#// Get audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):


    # #// Get saved audio file
    # audio_input = open("testVoice2.mp3", "rb")
    
    #// Save file from Frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #// Decode audio file
    message_decoded = convert_audio_to_text(audio_input)
    
    #// Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Message not decoded")
    
    #// Get ChatGPT response
    chat_response = get_chat_response(message_decoded)

    #// Guard: Ensure message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")


    #// Store messages
    store_messages(message_decoded, chat_response)

    #// Convert chat response to audio
    print(chat_response)
    audio_output = convert_text_to_speech(chat_response)

    #// Guard: Ensure message decoded
    if not audio_input:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")


    #// Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #// Return audio file
    return StreamingResponse(iterfile(), media_type="application/octet-stream")



# #// Post bot response
# #// Note: Not playing in browser when using post request
# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):

#     print("Hello")