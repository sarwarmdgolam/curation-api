# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.urls import reverse
# from unittest.mock import patch
#
# class AISummaryTests(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username="test", password="123456")
#         token = RefreshToken.for_user(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
#
#     @patch("app.contents.views.summarize_content")
#     def test_ai_summary(self, mock_summarize):
#         mock_summarize.return_value = "This is a summary."
#         data = {
#             "text": "Artificial Intelligence is transforming the world..."
#         }
#         response = self.client.post(reverse("ai-summary"), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["summary"], "This is a summary.")
#
#     @patch("app.contents.views.analyze_sentiment")
#     def test_sentiment(self, mock_sentiment):
#         mock_sentiment.return_value = "positive"
#         response = self.client.post(reverse("ai-sentiment"), {"text": "I love it!"})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["sentiment"], "positive")
#
#     @patch("app.contents.views.extract_topics")
#     def test_topic_extraction(self, mock_topics):
#         mock_topics.return_value = ["AI", "Innovation"]
#         response = self.client.post(reverse("ai-topics"), {"text": "AI drives innovation"})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("AI", response.data["topics"])
