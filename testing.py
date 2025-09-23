import requests
import json

BASE_URL = "http://127.0.0.1:8000"
conversation_id = "001"

OUTPUT_FILE = "TestResults"

def _write_raw(text: str, mode: str = "a"):
    with open(OUTPUT_FILE, mode, encoding="utf-8") as f:
        f.write(text)

# Overwrite the file at the start of every run
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("Memory Service Test Results\n")

def log_block(title: str, payload):
    """Print to terminal and append pretty JSON to TestResults file."""
    pretty = json.dumps(payload, indent=2)
    print(f"\n\n{title}:")
    print(pretty)
    _write_raw(f"\n\n{title}:\n")
    _write_raw(pretty + "\n")

def log_header(title: str):
    """Print & write a simple section header."""
    print(f"\n\n{title}")
    _write_raw(f"\n\n{title}\n")

#------------------------
log_header("Test 1 (Example)")

# Post
post_data = {
    "foo": "bar",
    "k2": {"sk3": 15, "sk4": None},
    "k3": [1, 2, 3, "foo"]
}
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=post_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Post", response.json())

# Update
update_data = {
    "k2": {"sk4": "val4", "sk5": 42},
    "k3": None,
    "k10": "val10"
}
log_block("GET Update Value", update_data)
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=update_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Update Result", response.json())

# Delete
del_resp = requests.delete(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
_write_raw(f"DELETE status: {del_resp.status_code}\n")
print(f"DELETE status: {del_resp.status_code}")
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET After Delete", response.json())

#------------------------
log_header("Test 2")

# Post
post_data = {
    "user": {
        "name": "Alice",
        "contacts": {
            "email": "alice@example.com",
            "phones": ["111-222-3333", "444-555-6666"]
        }
    },
    "roles": ["viewer", "editor"]
}
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=post_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Post", response.json())

# Update
update_data = {
    "user": {
        "contacts": {
            "email": "alice.new@example.com",
            "phones": ["999-888-7777"]
        }
    },
    "roles": ["admin"],
    "active": True
}
log_block("GET Update Value", update_data)
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=update_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Update Result", response.json())

# Delete
del_resp = requests.delete(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
_write_raw(f"DELETE status: {del_resp.status_code}\n")
print(f"DELETE status: {del_resp.status_code}")
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET After Delete", response.json())

#------------------------
log_header("Test 3")

# Post
post_data = {
    "order": {
        "id": 1234,
        "items": [
            {"product": "Book", "price": 10},
            {"product": "Pen", "price": 2}
        ],
        "status": "pending"
    },
    "notes": "Customer prefers morning delivery"
}
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=post_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Post", response.json())

# Update
update_data = {
    "order": {"status": "shipped", "items": None},
    "notes": None,
    "tracking": "XYZ-123-TRACK"
}
log_block("GET Update Value", update_data)
requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data", json=update_data)
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET Update Result", response.json())

# Delete
del_resp = requests.delete(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
_write_raw(f"DELETE status: {del_resp.status_code}\n")
print(f"DELETE status: {del_resp.status_code}")
response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/public-data")
log_block("GET After Delete", response.json())
