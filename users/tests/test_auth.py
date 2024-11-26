# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.test import TestCase

# class AuthenticationTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.username = 'testuser'
#         self.password = 'testpassword'
#         self.user_data = {
#             'username': self.username,
#             'password': self.password
#         }
#         self.user = User.objects.create_user(**self.user_data)

#     def test_user_registration(self):
#         url = reverse('api-register') 
#         data = {
#             'username': 'newuser',
#             'password': 'newpassword'
#         }

#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 2)

#     def test_user_login(self):
#         url = reverse('token_obtain_pair')
#         data = {
#             'username': self.username,
#             'password': self.password
#         }
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', response.data)
#         self.assertIn('refresh', response.data)

#     def test_protected_view_access(self):
#         url = reverse('protected-view')
#         refresh = RefreshToken.for_user(self.user)
#         headers = {'Authorization': f'Bearer {refresh.access_token}'}

#         response = self.client.get(url, HTTP_AUTHORIZATION=headers)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'This is a protected view.')

#     def test_protected_view_unauthenticated(self):
#         url = reverse('protected-view')

#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        

#     def test_logout(self):
#         url = reverse('logout') 
#         refresh = RefreshToken.for_user(self.user)
#         headers = {'Authorization': f'Bearer {refresh.access_token}'}

#         response = self.client.post(url, HTTP_AUTHORIZATION=headers)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Successfully logged out')
