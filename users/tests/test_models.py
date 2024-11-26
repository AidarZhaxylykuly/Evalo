from django.test import TestCase
from django.contrib.auth.models import User
from users.models import TestsFolder

class TestsFolderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_folder_creation(self):
        folder = TestsFolder.objects.create(owner=self.user, folder_name='Test Folder')

        self.assertEqual(folder.folder_name, 'Test Folder')
        self.assertEqual(folder.owner, self.user)
        self.assertTrue(isinstance(folder, TestsFolder))
        self.assertEqual(str(folder), f"Folder: Test Folder by {self.user.username}")

