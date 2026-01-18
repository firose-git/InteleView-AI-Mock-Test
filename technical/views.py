from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TechnicalQuestion, TechnicalAttempt
from .serializers import TechnicalQuestionSerializer
import random

# ✅ HTML Page
from django.middleware.csrf import get_token

@login_required
def technical_ui(request):
    csrf_token = get_token(request)
    # Fetch questions via API or directly
    response = get_technical_questions(request)
    if response.status_code == 200:
        questions = response.data
    else:
        questions = []
    return render(request, 'technical/technical_round.html', {'csrf_token': csrf_token, 'questions': questions})


# ✅ Get Questions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_technical_questions(request):
    user = request.user
    attempted_ids = list(
        TechnicalAttempt.objects.filter(user=user).values_list('question_id', flat=True)
    )
    attempted_ids = [str(i) for i in attempted_ids]

    all_questions = list(TechnicalQuestion.objects.all())
    unattempted_questions = [q for q in all_questions if str(q.id) not in attempted_ids]

    random.shuffle(unattempted_questions)
    selected_questions = unattempted_questions[:50]

    if not selected_questions:
        return Response({"error": "No new questions available."}, status=204)

    serializer = TechnicalQuestionSerializer(selected_questions, many=True)
    print("Serialized data:", serializer.data)  # Add debug print
    return Response(serializer.data)


# ✅ Submit Answer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_technical_answer(request):
    user = request.user
    data = request.data
    try:
        question = TechnicalQuestion.objects.get(id=data['question_id'])
    except TechnicalQuestion.DoesNotExist:
        return Response({"error": "Invalid question ID"}, status=400)

    attempt = TechnicalAttempt(user=user, question=question)

    if question.question_type == 'mcq':
        selected_option = data.get('selected_option')
        if not selected_option:
            return Response({"error": "No option selected"}, status=400)
        attempt.selected_option = selected_option
        attempt.is_correct = (selected_option == question.correct_answer)
        attempt.score = 1 if attempt.is_correct else 0

    elif question.question_type == 'code':
        code = data.get('submitted_code', '').strip()
        if not code:
            return Response({"error": "No code submitted"}, status=400)
        attempt.submitted_code = code
        attempt.is_correct = "def" in code  # Dummy logic
        attempt.score = 5 if attempt.is_correct else 0

    attempt.save()
    return Response({"status": "submitted", "score": attempt.score})

# ✅ Results Page
@login_required
def technical_result(request):
    user = request.user
    attempts = TechnicalAttempt.objects.filter(user=user).select_related('question').order_by('-attempted_at')[:50]

    total_score = sum(a.score for a in attempts)
    total_questions = attempts.count()

    # Annotate each attempt with answer and correct text (for direct use in template)
    for a in attempts:
        if a.selected_option and a.question.options:
            a.selected_option_text = a.question.options.get(a.selected_option, '')
        else:
            a.selected_option_text = 'Code Submitted'

        if a.question.correct_answer and a.question.options:
            a.correct_answer_text = a.question.options.get(a.question.correct_answer, '')
        else:
            a.correct_answer_text = ''

    return render(request, 'technical/technical_result.html', {
        'attempts': attempts,
        'total_score': total_score,
        'total_questions': total_questions
    })
