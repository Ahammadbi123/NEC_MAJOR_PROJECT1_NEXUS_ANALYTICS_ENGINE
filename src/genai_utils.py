import os
from groq import Groq
from dotenv import load_dotenv

# .env ఫైల్ ని లోడ్ చేస్తున్నాం
load_dotenv()

def get_ai_advice(query, data_summary):
    # .env ఫైల్ నుండి కీస్ ని తీసుకుంటున్నాం
    keys_env = os.getenv("GROQ_KEYS")
    
    if not keys_env:
        return "⚠️ Error: No API keys found in .env file."
        
    # కీస్ ని లిస్ట్ లాగా మారుస్తున్నాం
    GROQ_KEYS = [k.strip() for k in keys_env.split(",")]
    MODEL_NAME = "llama-3.3-70b-versatile"
    
    # ఒక్కో కీ ని ట్రై చేస్తున్నాం
    for api_key in GROQ_KEYS:
        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": f"Data: {data_summary}. Query: {query}"}],
                temperature=0.6,
                max_tokens=600
            )
            return completion.choices[0].message.content
        except Exception:
            continue # ఒక కీ ఫెయిల్ అయితే నెక్స్ట్ దానికి వెళ్ళు
            
    return "🤖 NEXUS AI: All keys are currently busy."