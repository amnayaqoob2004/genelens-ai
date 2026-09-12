import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Using openai/gpt-oss-120b — a strong, fast, free-tier-friendly model on Groq
MODEL_NAME = "openai/gpt-oss-120b"


def test_connection():
    """
    Send a simple test message to Groq to confirm the API key and connection work.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Say 'GeneLens AI is connected!' and nothing else."}
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Groq: {e}"