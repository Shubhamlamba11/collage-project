import os
import time
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.ai_engine import ai_engine_instance
from app.memory import memory_store
from app.tools import get_system_info, get_current_time_and_date, execute_math

app = FastAPI(
    title="J.A.R.V.I.S. AI Command System",
    description="Advanced AI assistant with Gemini LLM integration, voice interface, system utilities, and conversation memory.",
    version="2.0.0"
)

# Request models
class QueryRequest(BaseModel):
    message: str
    api_key: Optional[str] = None

class ConfigRequest(BaseModel):
    gemini_api_key: str

class MathRequest(BaseModel):
    expression: str

# API Endpoints
@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    if request.api_key:
        ai_engine_instance.set_api_key(request.api_key)

    start_time = time.time()
    response_text = await ai_engine_instance.process_query_async(request.message)
    latency_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "status": "success",
        "query": request.message,
        "response": response_text,
        "latency_ms": latency_ms,
        "timestamp": time.time()
    }

@app.get("/api/history")
async def get_history():
    return {
        "status": "success",
        "history": memory_store.get_formatted_history()
    }

@app.delete("/api/history")
async def clear_history():
    memory_store.clear()
    return {
        "status": "success",
        "message": "Conversation history cleared."
    }

@app.get("/api/system/status")
async def system_status():
    sys_info = get_system_info()
    sys_info["time"] = get_current_time_and_date()
    sys_info["has_gemini_key"] = bool(ai_engine_instance.gemini_client.api_key)
    return {
        "status": "success",
        "system_info": sys_info
    }

@app.post("/api/math")
async def math_eval(request: MathRequest):
    result = execute_math(request.expression)
    return {
        "status": "success",
        "result": result
    }

@app.post("/api/config")
async def set_config(request: ConfigRequest):
    if not request.gemini_api_key.strip():
        raise HTTPException(status_code=400, detail="API Key cannot be empty.")
    ai_engine_instance.set_api_key(request.gemini_api_key.strip())
    return {
        "status": "success",
        "message": "Gemini API key updated successfully."
    }

# Mount static files directory for frontend UI
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return JSONResponse({"message": "J.A.R.V.I.S. Core API Operational. UI under construction."})
