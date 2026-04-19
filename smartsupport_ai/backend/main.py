import os
import time
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from smartsupport_ai.db.database import init_db
from smartsupport_ai.rag.agent import multimodal_agent
from smartsupport_ai.core.observability import logger

app = FastAPI(
    title="SmartSupport Enterprise API",
    version="2.0.0",
    docs_url="/api/docs"
)

# 1. Prometheus Metrics Endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 2. Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Enterprise Database...")
    init_db()

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0", "timestamp": time.time()}

@app.post("/api/v1/chat")
async def chat_v2(request: Request):
    # Enterprise-grade chat endpoint with tracing
    form_data = await request.form()
    customer_id = form_data.get("customer_id")
    message = form_data.get("message")
    
    if not customer_id or not message:
        raise HTTPException(status_code=400, detail="Missing required fields")

    logger.info(f"Chat Request | Customer: {customer_id}")
    
    # Process using our Multi-Model Agent
    result = multimodal_agent.process_chat(customer_id, message)
    
    return JSONResponse(content=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
