import os, requests
from dotenv import load_dotenv


load_dotenv()


key = os.environ.get("OPENAI_API_KEY")
print("KEY LOADED:", key[:8], "...")  


r = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Hello from test!"}]
    }
)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)
