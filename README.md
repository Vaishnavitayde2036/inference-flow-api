# InferenceFlow API

A high-performance ML inference gateway built with FastAPI, designed for low-latency and high reliability.

## Key Features
- **Input Validation:** Uses Pydantic to enforce data types and prompt constraints.
- **In-Memory Caching:** Implements a cache layer to reduce redundant GPU compute for identical prompts.
- **Observability:** Built-in health checks and latency tracking for Prometheus monitoring.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn main:app --reload`
3. Access interactive docs: `http://127.0.0.1:8000/docs`

## Failure Modes Considered
1. **Model Overload:** Handled via async request handling.
2. **Invalid Input:** Automated 422 errors for malformed JSON.
3. **Cache Miss:** Graceful fallback to simulated inference engine.