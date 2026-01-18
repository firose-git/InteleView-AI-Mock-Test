from rest_framework import serializers
from .models import TechnicalQuestion, TechnicalAttempt

class TechnicalQuestionSerializer(serializers.ModelSerializer):
    options = serializers.JSONField()      # ✅ Ensure dict is handled
    test_cases = serializers.JSONField()   # ✅ Ensure list/dict is handled

    class Meta:
        model = TechnicalQuestion
        fields = ['id', 'question_type', 'question_text', 'options', 'test_cases', 'domain', 'difficulty']

class TechnicalAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalAttempt
        fields = '__all__'
