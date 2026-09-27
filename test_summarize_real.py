import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY)
prompt = "Summarize the following text:\n\nThe quick brown fox jumps over the lazy dog."

print(f"Testing model: {GEMINI_MODEL}")
response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
print(f"Response: {response.text}")
