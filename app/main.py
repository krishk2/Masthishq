import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Suppress TF Info/Warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# print("DEBUG: Importing API Router...", flush=True)
from app.api.endpoints import router as api_router 
# print("DEBUG: Importing Chat Endpoint...", flush=True)
from app.api import chat_endpoint 
# print("DEBUG: Imports Done.", flush=True) 

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for dashboard)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(chat_endpoint.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Memory for the Forgotten API is running"}

from fastapi.responses import HTMLResponse
@app.get("/report", response_class=HTMLResponse)
async def get_report_page():
    with open("app/templates/report.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
