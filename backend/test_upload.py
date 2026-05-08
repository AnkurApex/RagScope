import requests

with open("test.txt", "w") as f:
    f.write("This is a test document.")

with open("test.txt", "rb") as f:
    response = requests.post("http://127.0.0.1:8000/api/ingest/", files={"file": f})

print("Status:", response.status_code)
print("Response:", response.text)
