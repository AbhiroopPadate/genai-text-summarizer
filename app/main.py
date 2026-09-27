import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Text Summarizer")

# Setup templates and static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Define request model
class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

# Retrieve settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Configure Gemini Client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the frontend HTML."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_text(req: SummarizeRequest):
    """Summarize the provided text using Gemini API."""
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API key is not configured.")

    try:
        prompt = f"Summarize the following text concisely. Keep important points and use clear language. Use bullet points where appropriate:\n\n{req.text}"
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        summary = response.text
        return SummarizeResponse(summary=summary)
    
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the summary.")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

