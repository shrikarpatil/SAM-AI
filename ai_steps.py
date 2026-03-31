import os
from prompt import system_prompt
from prompt import get_prompt
from openai import OpenAI
from load_dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

client = OpenAI(api_key=api_key)

def generate_response(entitlements, elp, rhel, vdc) -> str:    
     prompt = get_prompt(entitlements, elp, rhel, vdc)
     response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=800,     
        timeout=60 
    )
     return response.choices[0].message.content

