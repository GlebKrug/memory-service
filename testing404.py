import requests

BASE_URL = "http://127.0.0.1:8000"
conversation_id = "001"


print("\n\nTest 1 – Missing Keys (should return 404)")

cid = "demo-404"

r = requests.get(f"{BASE_URL}/v1/conversations/{cid}/public-data")
print("GET missing public:", r.status_code, r.json())

r = requests.delete(f"{BASE_URL}/v1/conversations/{cid}/public-data")
print("DELETE missing public:", r.status_code, r.json())


print("\n\nTest 2 – Delete works (204 then 404)")

cid = "demo-204"

r = requests.post(f"{BASE_URL}/v1/conversations/{cid}/public-data", json={"foo": "bar"})
print("POST create:", r.status_code, r.json())

r = requests.delete(f"{BASE_URL}/v1/conversations/{cid}/public-data")
print("DELETE existing:", r.status_code, "Body:", repr(r.text))

r = requests.get(f"{BASE_URL}/v1/conversations/{cid}/public-data")
print("GET after delete:", r.status_code, r.json())


print("\n\nTest 3 – Invalid Body (should return 422)")

cid = "demo-422"


r = requests.post(
    f"{BASE_URL}/v1/conversations/{cid}/public-data",
    json=["this", "is", "not", "an", "object"]
)
print("POST invalid body:", r.status_code, r.json())
