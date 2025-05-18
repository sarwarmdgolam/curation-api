from unittest.mock import patch

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from app.contents.models import Content, Category
from django.urls import reverse


class ContentAPITests(APITestCase):

    fixtures = ['app/contents/fixtures.yaml']

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123456")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_category_count(self):
        count = Category.objects.count()
        self.assertEqual(count, 2)

    @patch("app.contents.tasks.background.process_content.apply_async")
    def test_create_content(self, mock_apply_async):
        url = reverse("content-list")
        category = Category.objects.get(pk=1)
        data = {
            "title": "AI Revolution",
            "body": "AI is transforming the world.",
            "category": category.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Content.objects.count(), 1)

        content_id = response.data.get("id")
        mock_apply_async.assert_called_once_with(args=[content_id])

    def test_list_contents(self):
        category = Category.objects.get(pk=1)
        Content.objects.create(author=self.user, title="1", body="Body", category=category)
        response = self.client.get(reverse("content-list"))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
