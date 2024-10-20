from django.contrib import admin
from .models import Profile, Follow, TestsFolder

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(TestsFolder)