import time
import asyncio
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="InferenceFlow API")

# --- PHASE 2: SCHEMAS (Input Validation) ---
class InferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500, example="Why is the sky blue?")
    model_name: str = Field(default="gpt-light-v1")
    temperature: float = Field(default=0.7, ge=0, le=1.0)

class InferenceResponse(BaseModel):
    id: str
    output: str
    latency_ms: float
    cached: bool

# --- MOCK LAYERS (Simulating Redis and ML Model) ---
mock_redis_cache = {}

async def simulate_inference(prompt: str):
    # Simulate GPU processing time
    await asyncio.sleep(1.5) 
    return f"Processed result for: {prompt}"

# --- API ENDPOINTS ---
@app.post("/v1/predict", response_model=InferenceResponse)
async def predict(request: InferenceRequest):
    start_time = time.perf_counter()
    
    # 1. Check Cache Layer (Redis)
    cache_key = f"{request.model_name}:{request.prompt}"
    if cache_key in mock_redis_cache:
        latency = (time.perf_counter() - start_time) * 1000
        return {
            "id": "res_cache_123",
            "output": mock_redis_cache[cache_key],
            "latency_ms": round(latency, 2),
            "cached": True
        }

    # 2. Inference Layer (If Cache Miss)
    try:
        result = await simulate_inference(request.prompt)
        
        # Save to Cache for next time
        mock_redis_cache[cache_key] = result
        
        latency = (time.perf_counter() - start_time) * 1000
        return {
            "id": "res_inf_456",
            "output": result,
            "latency_ms": round(latency, 2),
            "cached": False
        }
    except Exception as e:
        # Observability: In a real app, log this error to Prometheus
        raise HTTPException(status_code=500, detail="Inference Engine Failure")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}