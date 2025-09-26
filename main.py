from fastapi import FastAPI, Header, HTTPException
from typing import Optional
import logging
import threading
from logging.handlers import RotatingFileHandler


app = FastAPI()

storage = {}


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')
logger = logging.getLogger("memory-service")
handler = RotatingFileHandler("memory-service.log", maxBytes=1_000_000, backupCount=3)
logger.addHandler(handler)


_locks = {}
_global_lock = threading.Lock()

def _get_lock(key):
    with _global_lock:
        if key not in _locks:
            _locks[key] = threading.Lock()
        return _locks[key]


def _log(event: str, conversation_id: str, corr: str | None):
    logger.info(f"[corr={corr}] {event} cid={conversation_id}")

def check_key(conversation_id: str, visibility: str):
    key = (conversation_id, visibility)
    if key not in storage:
        raise HTTPException(status_code=404, detail="conversation_id not found")
    return key

def deep_merge(existing, update):
    if update is None:
        return None
    if isinstance(existing, dict) and isinstance(update, dict):
        result = dict(existing)
        for k, v in update.items():
            result[k] = deep_merge(existing.get(k), v)
        return result
    if isinstance(update, list):
        return list(update)
    return update

@app.get("/healthcheck")
def healthcheck():
    return {"status": "working"}

@app.get("/v1/conversations/{conversation_id}/public-data")
def get_public(conversation_id: str, aplm_correlation_id: Optional[str] = Header(None)):
    _log("GET /public-data", conversation_id, aplm_correlation_id)
    key = check_key(conversation_id, "public")
    return storage[key]

@app.post("/v1/conversations/{conversation_id}/public-data")
def update_public(conversation_id: str, data: dict, aplm_correlation_id: Optional[str] = Header(None)):
    _log("POST /public-data", conversation_id, aplm_correlation_id)
    key = (conversation_id, "public")
    lock = _get_lock(key)
    with lock:
        existing = storage.get(key, {})
        merged = deep_merge(existing, data)
        storage[key] = merged
    return merged

@app.delete("/v1/conversations/{conversation_id}/public-data", status_code=204)
def delete_public(conversation_id: str, aplm_correlation_id: Optional[str] = Header(None)):
    _log("DELETE /public-data", conversation_id, aplm_correlation_id)
    key = check_key(conversation_id, "public")
    storage.pop(key)

#-------------------------

@app.get("/v1/conversations/{conversation_id}/private-data")
def get_private(conversation_id: str, aplm_correlation_id: Optional[str] = Header(None)):
    _log("GET /private-data", conversation_id, aplm_correlation_id)
    key = check_key(conversation_id, "private")
    return storage[key]

@app.post("/v1/conversations/{conversation_id}/private-data")
def update_private(conversation_id: str, data: dict, aplm_correlation_id: Optional[str] = Header(None)):
    _log("POST /private-data", conversation_id, aplm_correlation_id)
    key = (conversation_id, "private")
    lock = _get_lock(key)
    with lock:
        existing = storage.get(key, {})
        merged = deep_merge(existing, data)
        storage[key] = merged
    return merged

@app.delete("/v1/conversations/{conversation_id}/private-data", status_code=204)
def delete_private(conversation_id: str, aplm_correlation_id: Optional[str] = Header(None)):
    _log("DELETE /private-data", conversation_id, aplm_correlation_id)
    key = check_key(conversation_id, "private")
    storage.pop(key)
#-------------------------



