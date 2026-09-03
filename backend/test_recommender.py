import httpx

response = httpx.get('http://127.0.0.1:8000/recommendations/', headers={'Authorization': 'Bearer placeholder'})
print("Status Code:", response.status_code)
print("Response:", response.text)
