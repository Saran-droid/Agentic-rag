from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqLLM:
    def __init__(self, model: str = None):
        self.model = model or os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    def invoke(self, prompt: str) -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

groq_llm = GroqLLM()
