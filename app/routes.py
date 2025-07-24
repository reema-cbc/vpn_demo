from fastapi import APIRouter, HTTPException, Request,Body
from pydantic import BaseModel, HttpUrl,constr
from app.youtube_trancription import  get_youtube_transcript
# from app.services.loom_transcript import get_loom_transcript
# from app.services.awesomess_transcript import get_awesomess_transcript
# from app.services.zoom_transcript import get_zoom_transcript

from app.utils.utils import detect_video_source
from app.groq import (
    generate_tasks_from_transcript_with_groq,
    format_bullet_tasks_dot_prefix,generate_tasks_from_large_transcript  
)

from pydantic import BaseModel
# from typing import List
import time
from fastapi.responses import StreamingResponse
import httpx 


# request model for action_points:
class TranscriptBody(BaseModel):
    transcript: str

# request model for Trancriptions:
class TranscriptionRequest(BaseModel):
    url: HttpUrl
    # url: constr(strip_whitespace=True)
    
class StatusUpdateRequest(BaseModel):
    step: str
router = APIRouter()
# current_status = {"step": "Waiting for input...","source":""}

# Modify send_status_update to update current_status
# async def send_status_update(message: str, source: str):
#     try:
#         current_status["step"] = message
#         current_status["source"]= source # update status
#         print(f"[STATUS] Step: {message} | Source: {source}")
#         async with httpx.AsyncClient() as client:
#             await client.post("http://localhost:8000/api/v1/internal-status-update", json={"step": message})
#     except Exception as e:
#         print(f"Failed to send status: {e}")
                        
@router.post("/transcribe")
async def transcribe_video(request: TranscriptionRequest):
    # Guard: if user didn’t paste any URL
    if not request.url or str(request.url).strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Please paste a video URL."
        )    
       
    try:
        
        url = str(request.url)
        # await send_status_update("video received","")
        source = detect_video_source(url)
        # time.sleep(2)
        # await asyncio.sleep(2)
        # await send_status_update(f"source detected: {source}",source)
     

        if source == "youtube":
            transcript =  get_youtube_transcript(url)
        # elif source == "loom":
        #     transcript = get_loom_transcript(url)
        # elif source == "awesomess":
        #     transcript = get_awesomess_transcript(url)    
        # # elif source == "zoom":
        #     transcript = get_zoom_transcript(url)    
        else:
            # await send_status_update("unsupported video source","")
            raise HTTPException(status_code=400, detail="Unsupported video source")

        # Get task from Groq
        # raw_task = generate_tasks_from_transcript_with_groq(transcript=transcript)

        #  Format it into a list of clean .-bullets
        # formatted_task = format_bullet_tasks_dot_prefix(raw_task)
        # await send_status_update("All steps completed","")
        return {
            "source": source,
            "transcript": transcript,
            # "gen_task": formatted_task  # final response is clean list
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str("url is invalid"))
    except HTTPException as http_exc:
        print(f"http_exc: {http_exc}")
        raise http_exc
    except Exception as e:
        print(f"e: {e}")
        raise HTTPException(status_code=500, detail=f"Error while transcribing video: {str(e)}")
    
      
# @router.get("/status-update")
# async def get_status():
#     return current_status


# #  Optional: internal endpoint to receive status (not needed if updating locally)
# @router.post("/internal-status-update")
# async def internal_status(step: str = Body(..., embed=True)):
#     current_status["step"] = step
#     return {"status": step}
 

      
# @router.post("/action_points")
# def action_from_transcript(body: TranscriptBody):
#     if not body.transcript.strip():
#         raise HTTPException(status_code=400, detail="Transcript is empty.")
    
#     try:
#         raw_task = generate_tasks_from_transcript_with_groq(body.transcript)
#         formatted = format_bullet_tasks_dot_prefix(raw_task)
#         return {"gen_task": formatted}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.post("/action_points")
def action_from_transcript(body: TranscriptBody):
    if not body.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty.")
    
    try:
        tasks = generate_tasks_from_large_transcript(body.transcript)
        return {"gen_task": tasks.split("\n")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


























































































































































































































    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @router.post("/transcribe")
# async def transcribe_video(request: TranscriptionRequest):
#     messages = []

#     try:
#         url = str(request.url)
#         msg = " URL received."
        
#         print(msg)
#         messages.append(msg)

#         source = detect_video_source(url)
#         msg = f" Detected video source: {source}"
#         print(msg)
#         messages.append(msg)

#         if source == "youtube":
#             msg = "Downloading YouTube video..."
#             print(msg)
#             messages.append(msg)

#             transcript = get_youtube_transcript(url)

#             msg = " Transcript generated from YouTube."
#             print(msg)
#             messages.append(msg)

#         elif source == "loom":
#             msg = "Downloading Loom video..."
#             print(msg)
#             messages.append(msg)

#             transcript = get_loom_transcript(url)

#             msg = "Transcript generated from Loom."
#             print(msg)
#             messages.append(msg)

#         elif source == "awesomess":
#             msg = "Downloading AwesomeScreenshot video..."
#             print(msg)
#             messages.append(msg)

#             transcript = get_awesomess_transcript(url)

#             msg = "Transcript generated from AwesomeScreenshot."
#             print(msg)
#             messages.append(msg)

#         else:
#             msg = "Unsupported video source."
#             print(msg)
#             messages.append(msg)
#             raise HTTPException(status_code=400, detail={"error": "Unsupported video source", "messages": messages})

#         return {
#             "messages": messages,
#             "source": source,
#             "transcript": transcript
#         }

#     except ValueError as ve:
#         msg = " URL is invalid."
#         print(msg)
#         messages.append(msg)
#         raise HTTPException(status_code=400, detail={"error": str(ve), "messages": messages})

#     except HTTPException as http_exc:
#         msg = " HTTP error occurred."
#         print(msg)
#         messages.append(msg)
#         raise HTTPException(status_code=http_exc.status_code, detail={"error": str(http_exc.detail), "messages": messages})

#     except Exception as e:
#         msg = f" Unexpected error during transcription: {str(e)}"
#         print(msg)
#         messages.append(msg)
#         raise HTTPException(status_code=500, detail={"error": str(e), "messages": messages})

    

