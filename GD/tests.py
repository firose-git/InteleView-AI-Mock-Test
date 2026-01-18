from django.test import TestCase, Client
from django.urls import reverse
from .ai_engine import generate_gd_topics, evaluate_response

class GDTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_generate_gd_topics(self):
        topics = generate_gd_topics()
        self.assertEqual(len(topics), 3)
        self.assertIsInstance(topics[0], str)

    def test_gd_home_view(self):
        response = self.client.get(reverse('GD:gd_home'))
        self.assertEqual(response.status_code, 200)

    def test_instruction_session_flow(self):
        # Step 1: get instructions
        response = self.client.get(reverse('GD:gd_instructions'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('topics', self.client.session)

        # Step 2: start session
        response = self.client.get(reverse('GD:gd_session'))
        self.assertEqual(response.status_code, 200)

    def test_evaluate_response_format(self):
        dummy_transcript = "AI is helping humans in many areas but can't fully replace creativity."
        topic = "Is AI replacing human creativity?"
        result = evaluate_response(dummy_transcript, topic)
        self.assertIn("fluency", result)
