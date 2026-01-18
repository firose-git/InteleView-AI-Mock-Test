from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
import json
import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# MongoDB connection
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["chatbot_db"]
chat_collection = db["chat_logs"]

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Prepare initial log
        session_key = request.session.session_key or request.session.save()
        log = {
            "session_id": session_key,
            "user_message": user_message,
            "bot_reply": "",
        }

        try:
            response = openai.ChatCompletion.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant for the InteleView AI Interview Portal."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response['choices'][0]['message']['content'].strip()

            # Store full conversation in MongoDB
            log["bot_reply"] = bot_reply
            chat_collection.insert_one(log)

            return JsonResponse({'response': bot_reply})
        except Exception as e:
            print("OpenRouter error:", e)
            return JsonResponse({'response': '⚠️ AI connection failed. Please try again later.'})
