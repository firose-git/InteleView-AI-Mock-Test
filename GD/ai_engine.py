import random
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")

def generate_gd_topics():
    return random.sample([
        "Is AI replacing human creativity?",
        "Should social media be regulated more strictly?",
        "Is remote work a long-term solution?",
        "Climate change: Individual action vs government policy",
        "Impact of digital payments on rural economy",
        "Does India need a two-party political system?",
        "Role of youth in national development",
        "Is traditional education becoming obsolete?",
        "Cybersecurity and ethical hacking: Boon or threat?",
        "Future of EVs in developing countries"
    ], 3)

def evaluate_response(transcript, topic):
    prompt = f"""
    Evaluate this response on: "{topic}"
    ---
    {transcript}
    ---
    Return JSON:
    {{
      "fluency": <score>,
      "vocabulary": <score>,
      "clarity": <score>,
      "confidence": <score>,
      "summary": "...",
      "suggestions": ["...", "..."]
    }}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message['content']
        return json.loads(content)
    except Exception as e:
        return {
            "fluency": 0, "vocabulary": 0, "clarity": 0, "confidence": 0,
            "summary": "Error generating evaluation.",
            "suggestions": [str(e)]
        }
