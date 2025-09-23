from fastapi import FastAPI
from fastapi import Header
from typing import Optional
from deep_merge import deep_merge

app = FastAPI()

storage = {}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "working"}

@app.get("/v1/conversations/{conversation_id}/public-data")
def get_public(conversation_id: str):
    return storage.get((conversation_id, "public"), {})

@app.post("/v1/conversations/{conversation_id}/public-data")
def update_public(conversation_id: str, data: dict, aplm_correlation_id: Optional[str] = Header(None)):
    if aplm_correlation_id:
        print(f"Correlation ID: {aplm_correlation_id}")
    existing = storage.get((conversation_id, "public"), {})
    merged = deep_merge(existing, data)
    storage[(conversation_id, "public")] = merged
    return merged

@app.delete("/v1/conversations/{conversation_id}/public-data")
def delete_public(conversation_id: str):
    storage.pop((conversation_id, "public"), None)
    return {}

@app.get("/v1/conversations/{conversation_id}/private-data")
def get_private(conversation_id: str):
    return storage.get((conversation_id, "private"), {})

@app.post("/v1/conversations/{conversation_id}/private-data")
def update_private(conversation_id: str, data: dict):
    existing = storage.get((conversation_id, "private"), {})
    merged = deep_merge(existing, data)
    storage[(conversation_id, "private")] = merged
    return merged

@app.delete("/v1/conversations/{conversation_id}/private-data")
def delete_private(conversation_id: str):
    storage.pop((conversation_id, "private"), None)
    return {}
