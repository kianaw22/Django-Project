from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('blog:signup')  # The URL name defined in your urls.py
        self.valid_payload = {
            "username": "new_user",
            "email": "new@yahoo.com",
            "password": "StrongPassword123",
            "role": "student"  # example role, if your serializer uses it
        }
        self.invalid_payload = {
            # Missing some required fields, or invalid data
            "username": "",
            "email": "not-an-email",
            "password": ""
        }
    def test_signup_success(self):
        """
        Test that providing valid data creates a new user and returns JWT tokens.
        """
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check response structure
        self.assertIn("message", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "new_user")

        # Check user was actually created
        self.assertTrue(User.objects.filter(username="new_user").exists())

class ChangeRoleViewTest(APITestCase):
    
    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            role='admin'  
        )
        self.normal_user = get_user_model().objects.create_user(
            username='normaluser',
            email='user@example.com',
            password='userpassword',
            role='user'  
        )
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.normal_user_token = RefreshToken.for_user(self.normal_user).access_token
        self.url = '/change_role/'  
    def test_change_role_as_admin(self):

        data = {
            'user_id': self.normal_user.id,
            'role': 'admin',  
        }

        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.post(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = get_user_model().objects.get(id=self.normal_user.id)
        self.assertEqual(updated_user.role, 'admin')

        self.assertEqual(response.data['message'], 'User role updated successfully.')

    def test_change_role_as_non_admin(self):

        data = {
            'user_id': self.normal_user.id,
            'role': 'admin',
        }

        # تنظیم هدر Authorization با توکن کاربر غیر ادمین
        headers = {
            'Authorization': f'Bearer {self.normal_user_token}'
        }

        # ارسال درخواست POST
        response = self.client.post(self.url, data, headers=headers, format='json')

        # اطمینان از اینکه وضعیت پاسخ 403 Forbidden است
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_role_as_unauthenticated_user(self):
        # داده برای تغییر نقش کاربر
        data = {
            'user_id': self.normal_user.id,
            'role': 'admin',
        }

        # ارسال درخواست بدون هدر Authorization
        response = self.client.post(self.url, data, format='json')

        # اطمینان از اینکه وضعیت پاسخ 401 Unauthorized است
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_user_id(self):
        # داده برای تغییر نقش با user_id نامعتبر
        data = {
            'user_id': 9999,  # فرض می‌کنیم این user_id وجود ندارد
            'role': 'admin',
        }

        # تنظیم هدر Authorization با توکن کاربر ادمین
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }

        # ارسال درخواست POST
        response = self.client.post(self.url, data, headers=headers, format='json')

        # اطمینان از اینکه وضعیت پاسخ 400 Bad Request است
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # اطمینان از اینکه پیغام خطای صحیح در پاسخ آمده است
        self.assertIn('User not found.', response.data['user_id'])
