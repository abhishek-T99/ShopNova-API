from django.urls import reverse
from allauth.account.models import EmailAddress
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import PhoneNumber

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "phone_number": "+9779840196929",
            "password1": "Password@123",
            "password2": "Password@123",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password1"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
            username=self.user_data["email"],
        )
        self.url_registration = reverse("users:user_register")
        self.url_login = reverse("users:user_login")

    def test_user_registration_with_email(self):
        """
        Ensure a user can register using email or phone number.
        """
        data = {
            "email": "testuser1@example.com",
            "password1": "MyPass@123",
            "password2": "MyPass@123",
            "first_name": "Test",
            "last_name": "User1",
        }

        response = self.client.post(self.url_registration, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_profile(self):
        """
        Test retrieving user profile.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/user/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_address(self):
        """
        Test retrieving user address.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/user/profile/address/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login_credentials(self):
        """
        Test login failure due to invalid credentials.
        """
        data = {
            "email": self.user_data["email"],
            "password": "wrongpassword",
        }

        response = self.client.post(self.url_login, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
