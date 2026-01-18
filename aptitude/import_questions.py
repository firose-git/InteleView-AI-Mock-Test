import json
from aptitude.models import AptitudeQuestion

with open('aptitude_questions.json') as f:
    data = json.load(f)

for item in data:
    AptitudeQuestion.objects.create(
        domain=item['domain'],
        section=item['section'],
        company=item['company'],
        question_text=item['question_text'],
        options=item['options'],
        answer=item['answer']
    )

print("✅ Questions uploaded successfully!")
