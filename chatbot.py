import os
from google import genai
from dotenv import load_dotenv

# Loading keys to environment
load_dotenv()

model_name = os.getenv('MODEL_NAME')

client = genai.Client()

def build_prompt(history, user_message):
    prompt = "SYSTEM: Be concise. Answer in one sentence only."
    
    for role, message in history:
        prompt += f"{role}: {message}\n"
        
    prompt += f"user: {user_message}\nassistant: "
    
    return prompt

def ask_gemini(history, user_message):
    prompt = build_prompt(history, user_message)
    
    response = client.interactions.create(
        model=model_name,
        input=prompt,
        generation_config={
        "temperature": 0.7
    }
    )
    
    return response.output_text