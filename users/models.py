from django.db import models
from django.contrib.auth.models import User
from tests.models import Test

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
<<<<<<< Updated upstream
    gpa = models.FloatField(default=0.0)
=======
    gpa = models.FloatField(null=True, blank=True)
>>>>>>> Stashed changes

    def __str__(self):
        return f'{self.user.username} Profile'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
        
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
class TestsFolder(models.Model):
    folder_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    test_blanks = models.ManyToManyField(Test, blank=True) 

    def __str__(self):
        return f'Folder: {self.folder_name} by {self.owner.username}'
