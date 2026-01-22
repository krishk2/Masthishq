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

# --- Frontend Serving (Deployment) ---
# Check if frontend build exists (Render/Production)
if os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Allow API calls to pass through
        if full_path.startswith("api"):
            return {"error": "Not Found"}
            
        # Serve index.html for SPA routing
        if "." not in full_path:
            return FileResponse("frontend/dist/index.html")
        
        # Serve other static files if they exist
        if os.path.exists(f"frontend/dist/{full_path}"):
             return FileResponse(f"frontend/dist/{full_path}")
             
        return FileResponse("frontend/dist/index.html")

@app.get("/")
def root():
    # If build exists, serve it
    if os.path.exists("frontend/dist/index.html"):
        return FileResponse("frontend/dist/index.html")
    return {"message": "Memory for the Forgotten API is running (Dev Mode)"}

from fastapi.responses import HTMLResponse, FileResponse
@app.get("/report", response_class=HTMLResponse)
async def get_report_page():
    if os.path.exists("app/templates/report.html"):
        with open("app/templates/report.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return {"error": "Report template not found"}
