# FastAPI and Dependencies
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

# API Models
from app.core.models import LinkRequest

# Exception Handler Decorator
from app.core.errors import exception_handler

# AI Processing
from app.ai.ai import process_transcript, validate_transcript

# Utilities
from app.utils import fetch_transcript, save_output_to_file, save_transcript_to_file, clean_up_logger, format_analyst_output

# Jinja2 Templates Setup
templates = Jinja2Templates(directory="templates")

# FastAPI App with lifespan for cleanup
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    clean_up_logger()

app = FastAPI(lifespan=lifespan)

# Root route to show the form
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# POST Endpoint to Process and Validate Transcript
@app.post("/process-transcript/", response_class=HTMLResponse)
@exception_handler
async def process_transcripts_endpoint(request: Request, link: str = Form(...)):
    """
    POST request to process and validate meeting transcripts into bulleted value pyramid for NBM.
    """
    # Fetch transcripts
    meeting_id, transcript = fetch_transcript(link)

    # Save transcripts to a JSON file
    save_transcript_to_file(transcript, meeting_id)

    # Process the transcript
    processed_transcript = process_transcript(transcript)

    # Validate the processed transcript
    validated_transcript = validate_transcript(processed_transcript)

    save_output_to_file(validated_transcript, meeting_id)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "message": "Meeting transcript processed successfully.",
            "meeting_id": meeting_id,
            "transcripts": format_analyst_output(validated_transcript)
        }
    )
