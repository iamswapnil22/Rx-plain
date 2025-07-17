import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def query_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful AI that explains medical prescriptions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
