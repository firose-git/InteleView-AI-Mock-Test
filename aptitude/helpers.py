from .models import AptitudeQuestion
import random

def get_filtered_questions(user):
    print("User Authenticated:", user.is_authenticated)
    print("User:", user.email)
    print("User domain:", getattr(user, 'user_type', None))

    try:
        user_type = getattr(user, 'user_type', None)
        if user_type == 'student':
            domain = 'IT'
        elif user_type in ['professional', 'trial']:
            domain = 'Non-IT'
        else:
            raise ValueError("Invalid or missing user_type")

        # ✅ Avoid order_by('?') — get all and shuffle in Python
        questions = list(AptitudeQuestion.objects.filter(domain=domain))
        random.shuffle(questions)
        return questions[:40]

    except Exception as e:
        import traceback
        print("Error in get_filtered_questions:", str(e))
        traceback.print_exc()
        return []
