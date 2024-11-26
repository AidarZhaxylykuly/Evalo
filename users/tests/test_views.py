from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from users.models import TestsFolder

class FolderApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.folder = TestsFolder.objects.create(owner=self.user, folder_name='Test Folder')

    def test_create_folder(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create-folder')
        data = {'folder_name': 'New Folder'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestsFolder.objects.count(), 2)

    def test_get_folder(self):
        url = reverse('folder-detail', kwargs={'folder_id': self.folder.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Folder')

    def test_delete_folder(self):
        url = reverse('delete-folder', kwargs={'folder_id': self.folder.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(TestsFolder.objects.count(), 0)
