from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os, json

from .ai_engine import generate_gd_topics, evaluate_response
from .whisper_utils import transcribe_audio_file

def gd_home(request):
    return render(request, 'gd/home.html')

def gd_instructions(request):
    topics = generate_gd_topics()
    request.session['gd_topics'] = topics
    return render(request, 'gd/instruction.html', {'topics': topics})

def gd_session(request):
    topics = request.session.get('gd_topics', [])
    return render(request, 'gd/session.html', {
        'topics': topics,
        'topic_number': 1,
        'topic': topics[0] if topics else "No topic found"
    })

def gd_results(request):
    transcript = request.session.get('gd_transcript', '')
    evaluation = request.session.get('gd_evaluation', {})
    return render(request, 'gd/result.html', {
        'transcript': transcript,
        'evaluation': evaluation
    })

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        file_path = "temp_audio.webm"
        try:
            with open(file_path, "wb+") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            transcript = transcribe_audio_file(file_path)
            topics = request.session.get('gd_topics', [])
            topic_index = int(request.POST.get("topic_index", 0))
            topic = topics[topic_index] if topic_index < len(topics) else "Unknown topic"
            evaluation = evaluate_response(transcript, topic)

            # Save to session
            request.session['gd_transcript'] = transcript
            request.session['gd_evaluation'] = evaluation

            return JsonResponse({
                'transcript': transcript,
                'evaluation': evaluation
            })

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# ✅ Accepts transcript + evaluation and stores it (you can later write DB logic)
@csrf_exempt
def submit_results(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            results = data.get('results', [])

            for entry in results:
                print("Topic:", entry.get("topic"))
                print("Transcript:", entry.get("transcript"))

            return JsonResponse({
                "status": "success",
                "message": "GD results submitted.",
                "data": results
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


