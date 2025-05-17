from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class AuthTests(APITestCase):
    def test_user_registration(self):
        url = reverse("register")
        data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.post(reverse("register"), {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        })

        url = reverse("token_obtain_pair")
        response = self.client.post(url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
