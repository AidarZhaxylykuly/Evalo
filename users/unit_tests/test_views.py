from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from users.models import Follow, TestsFolder

class FolderApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.login(username='testuser', password='testpassword')

        self.folder = TestsFolder.objects.create(owner=self.user, folder_name='Test Folder')

    def test_user_register_view(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2) 

    def test_follow_user_view(self):
        url = reverse('follow_user', kwargs={'user_id': self.user2.id})
        self.client.login(username='user1', password='password1')
        response = self.client.post(url)
        
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.user2).exists())
    
    def test_unfollow_user_view(self):
        Follow.objects.create(follower=self.user, following=self.user2)
        
        url = reverse('unfollow_user', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.user2).exists())
        
    def test_create_folder(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('create-folder')
        data = {'folder_name': 'New Folder'}    
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(TestsFolder.objects.count(), 2)

    def test_get_folder(self):
        url = reverse('folder-detail', kwargs={'folder_id': self.folder.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Folder')

    def test_edit_folder_view(self):
        folder = TestsFolder.objects.create(owner=self.user, folder_name='Test Folder')
        url = reverse('edit-folder', kwargs={'folder_id': folder.id})
        data = {'folder_name': 'Updated Folder'}
        response = self.client.post(url, data)
        
        folder.refresh_from_db()
        self.assertRedirects(response, reverse('folder-detail', kwargs={'folder_id': folder.id}))
        self.assertEqual(folder.folder_name, 'Updated Folder')

    def test_delete_folder(self):
        url = reverse('delete-folder', kwargs={'folder_id': self.folder.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(TestsFolder.objects.count(), 0)

    def test_unauthorized_access(self):
        url = reverse('create-folder')
        data = {'folder_name': 'Unauthorized Folder'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_folder_by_non_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        folder = TestsFolder.objects.create(owner=self.user, folder_name='Test Folder')

        self.client.login(username='anotheruser', password='anotherpassword')
        url = reverse('delete-folder', kwargs={'folder_id': folder.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    