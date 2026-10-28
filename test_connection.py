import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ API key not found. Please check your .env file.")
    exit()

print("🔄 Connecting to Groq servers...")

try:
    client = Groq(api_key=api_key)
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Explain what Python is in two sentences."}],
        model=model_name,
        timeout=15
    )
    
    print("✅ Connection successful! Model response:")
    print("-" * 40)
    print(response.choices[0].message.content)
    print("-" * 40)

except Exception as e:
    print(f"❌ An error occurred: {e}")