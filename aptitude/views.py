# aptitude/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AptitudeQuestion, AptitudeAttempt
from .helpers import get_filtered_questions
from django.utils import timezone
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def start_test_page(request):
    return render(request, 'aptitude/start_test.html')

@login_required
def start_test_logic(request):
    request.session['apt_question_ids'] = [q.id for q in get_filtered_questions(request.user)]
    request.session['apt_index'] = 0
    return redirect('aptitude:question_page')

# @csrf_exempt
# @login_required
# def log_cheating(request):
#     if request.method == "POST":
#         # Log user + timestamp
#         print(f"⚠️ Cheating suspected for {request.user.email} at {timezone.now()}")
#         return JsonResponse({"status": "logged"})
@csrf_exempt
@login_required
def log_cheating(request):
    if request.method == "POST":
        # Optional: log to model
        print(f"[Cheating] User {request.user} attempted suspicious activity.")
        return JsonResponse({"status": "logged"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def question_page(request):
    ids = request.session.get('apt_question_ids', [])
    index = request.session.get('apt_index', 0)

    if index >= len(ids):
        return redirect('aptitude:result')

    question_id = ids[index]
    question = AptitudeQuestion.objects.get(id=question_id)

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        is_correct = (selected_option == question.answer)

        AptitudeAttempt.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            attempted_at=timezone.now()
        )

        request.session['apt_index'] += 1
        return redirect('aptitude:question_page')

    options = question.options.copy()
    random.shuffle(options)

    return render(request, 'aptitude/question_page.html', {
        'question': question,
        'options': options,
        'index': index + 1,
        'total': len(ids)
    })


@login_required
def result_page(request):
    attempts = AptitudeAttempt.objects.filter(user=request.user).order_by('-attempted_at')[:40]
    correct_count = sum(1 for a in attempts if a.is_correct)

    score = (correct_count / 40) * 100  # Out of 100

    return render(request, 'aptitude/result_page.html', {
        'attempts': attempts,
        'score': round(score, 2)
    })
